import json
import os
import platform
import queue
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

APP_TITLE = "Dev Environment Booster - GUI (Catalog + Search)"

# ---------------- helpers ----------------
def which(cmd):
    from shutil import which as _which
    return _which(cmd)

def detect_pkg_mgr():
    sys = platform.system().lower()
    if sys == "windows" and which("winget"):
        return "winget"
    if sys == "linux":
        for cmd in ("apt", "dnf", "pacman"):
            if which(cmd):
                return cmd
    if sys == "darwin" and which("brew"):
        return "brew"
    return None

def run_cmd_capture(cmd, shell=False):
    return subprocess.run(cmd, capture_output=True, text=True, shell=shell)

def normalize_app_entry(app):
    """
    Accepts either:
      - "git"
      - {"id": "Git.Git", "name": "git"}
    Returns (label_for_UI, id_or_None, name_or_None)
    """
    if isinstance(app, str):
        return (app, None, app)
    if isinstance(app, dict):
        return (app.get("name") or app.get("id") or "unknown", app.get("id"), app.get("name"))
    return (str(app), None, str(app))

def is_ambiguous_winget(output: str) -> bool:
    text = (output or "").lower()
    return "multiple packages found" in text or "more than one package" in text

def is_installed(pkg_mgr, app_id=None, app_name=None):
    """Return True if installed, False if not, None if unknown."""
    try:
        if pkg_mgr == "winget":
            if app_id:
                r = run_cmd_capture(["winget", "list", "--id", app_id, "--exact"], shell=True)
                return r.returncode == 0 and app_id.lower() in (r.stdout + r.stderr).lower()
            if app_name:
                r = run_cmd_capture(["winget", "list", app_name, "--exact"], shell=True)
                out = (r.stdout + r.stderr).lower()
                return r.returncode == 0 and app_name.lower() in out
            return None

        name = app_id or app_name
        if not name:
            return None

        if pkg_mgr == "apt":
            return run_cmd_capture(["dpkg", "-s", name]).returncode == 0
        if pkg_mgr == "dnf":
            return run_cmd_capture(["rpm", "-q", name]).returncode == 0
        if pkg_mgr == "pacman":
            return run_cmd_capture(["pacman", "-Qi", name]).returncode == 0
        if pkg_mgr == "brew":
            return run_cmd_capture(["brew", "list", name]).returncode == 0
    except Exception:
        return None
    return None

def build_install_cmd(pkg_mgr, app_id=None, app_name=None):
    """Prefer ID to avoid ambiguity; fallback to name."""
    target = app_id or app_name
    if not target:
        return None
    if pkg_mgr == "winget":
        if app_id:
            return ["winget", "install", "--id", app_id, "--exact",
                    "--silent", "--accept-package-agreements", "--accept-source-agreements"]
        else:
            return ["winget", "install", app_name, "--exact",
                    "--silent", "--accept-package-agreements", "--accept-source-agreements"]
    if pkg_mgr == "apt":
        return ["sudo", "apt", "install", "-y", target]
    if pkg_mgr == "dnf":
        return ["sudo", "dnf", "install", "-y", target]
    if pkg_mgr == "pacman":
        return ["sudo", "pacman", "-S", "--noconfirm", target]
    if pkg_mgr == "brew":
        return ["brew", "install", target]
    return None

# ---------------- app ----------------
class BoosterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1140x680")
        self.minsize(1040, 600)

        self.pkg_mgr = detect_pkg_mgr()
        self.config_data = {"apps": [], "paths": []}
        self.current_config_path = None
        self.worker_thread = None
        self.log_queue = queue.Queue()
        self.stop_flag = threading.Event()

        # catalog (apps.info)
        self.catalog = []         # list of dicts {id, name, category?}
        self.catalog_filter = ""  # current search text
        self.catalog_loaded = False

        self._build_ui()
        self._load_catalog_auto()
        self._log(f"Detected package manager: {self.pkg_mgr or 'None'}")
        self._mark_clean()

        # shortcuts
        self.bind("<Control-s>", lambda e: self.save_config())
        self.bind("<Control-S>", lambda e: self.save_config_as())

    # ---------- UI ----------
    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(6, weight=1)

        # top bar
        top = ttk.Frame(self, padding=(10, 10, 10, 0))
        top.grid(row=0, column=0, sticky="ew")
        top.columnconfigure(1, weight=1)

        ttk.Label(top, text="Config file:").grid(row=0, column=0, sticky="w")
        self.path_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.path_var).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(top, text="Open…", command=self.load_config_dialog).grid(row=0, column=2, padx=(0, 6))
        ttk.Button(top, text="New", command=self.new_config).grid(row=0, column=3)
        ttk.Button(top, text="Save", command=self.save_config).grid(row=0, column=4, padx=(6, 6))
        ttk.Button(top, text="Save As…", command=self.save_config_as).grid(row=0, column=5)

        # editors + catalog row
        split = ttk.Frame(self, padding=10)
        split.grid(row=1, column=0, sticky="nsew")
        split.columnconfigure(0, weight=1)
        split.columnconfigure(1, weight=1)
        split.columnconfigure(2, weight=1)
        split.rowconfigure(1, weight=1)

        # apps panel
        apps_frame = ttk.LabelFrame(split, text="Apps in Current Config", padding=8)
        apps_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 6))
        apps_frame.columnconfigure(0, weight=1)
        apps_frame.rowconfigure(0, weight=1)

        self.apps_list = tk.Listbox(apps_frame, selectmode="extended")
        self.apps_list.grid(row=0, column=0, sticky="nsew")

        app_edit = ttk.Frame(apps_frame)
        app_edit.grid(row=1, column=0, sticky="ew", pady=6)
        app_edit.columnconfigure(1, weight=1)

        ttk.Label(app_edit, text="Add app (name or exact ID):").grid(row=0, column=0, sticky="w")
        self.new_app_var = tk.StringVar()
        ttk.Entry(app_edit, textvariable=self.new_app_var).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(app_edit, text="Add (name)", command=self.add_app_by_name).grid(row=0, column=2)
        ttk.Button(app_edit, text="Add (id)", command=self.add_app_by_id).grid(row=0, column=3, padx=(6,0))
        ttk.Button(app_edit, text="Remove Selected", command=self.remove_selected_apps).grid(row=0, column=4, padx=(6,0))

        # paths panel
        paths_frame = ttk.LabelFrame(split, text="Directories to Create", padding=8)
        paths_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=6)
        paths_frame.columnconfigure(0, weight=1)
        paths_frame.rowconfigure(0, weight=1)

        self.paths_list = tk.Listbox(paths_frame, selectmode="extended")
        self.paths_list.grid(row=0, column=0, sticky="nsew")

        path_edit = ttk.Frame(paths_frame)
        path_edit.grid(row=1, column=0, sticky="ew", pady=6)
        path_edit.columnconfigure(1, weight=1)

        ttk.Label(path_edit, text="New path:").grid(row=0, column=0, sticky="w")
        self.new_path_var = tk.StringVar()
        ttk.Entry(path_edit, textvariable=self.new_path_var).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(path_edit, text="Browse…", command=self.pick_folder_for_path).grid(row=0, column=2)
        ttk.Button(path_edit, text="Add", command=self.add_path).grid(row=0, column=3, padx=(6,0))
        ttk.Button(path_edit, text="Remove Selected", command=self.remove_selected_paths).grid(row=0, column=4, padx=(6,0))

        # catalog panel
        catalog_frame = ttk.LabelFrame(split, text="Catalog (apps.info)", padding=8)
        catalog_frame.grid(row=0, column=2, sticky="nsew", padx=(6, 0))
        catalog_frame.columnconfigure(0, weight=1)
        catalog_frame.rowconfigure(2, weight=1)

        # search bar
        search_row = ttk.Frame(catalog_frame)
        search_row.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        search_row.columnconfigure(1, weight=1)
        ttk.Label(search_row, text="Search:").grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        e = ttk.Entry(search_row, textvariable=self.search_var)
        e.grid(row=0, column=1, sticky="ew", padx=6)
        e.bind("<KeyRelease>", lambda _e: self._refresh_catalog_list())
        ttk.Button(search_row, text="Reload", command=self._load_catalog_auto).grid(row=0, column=2)

        # catalog list
        self.catalog_list = tk.Listbox(catalog_frame, selectmode="extended")
        self.catalog_list.grid(row=2, column=0, sticky="nsew")
        self.catalog_list.bind("<Double-Button-1>", lambda _e: self.add_from_catalog_double())
        self.catalog_list.bind("<Return>", lambda _e: self.add_from_catalog_double())

        # add button
        ttk.Button(catalog_frame, text="Add Selected to Config →", command=self.add_from_catalog_selected)\
            .grid(row=3, column=0, sticky="e", pady=(6,0))

        # options + actions
        opts = ttk.Frame(self, padding=(10, 0, 10, 0))
        opts.grid(row=2, column=0, sticky="ew")
        opts.columnconfigure(0, weight=1)

        self.dry_run = tk.BooleanVar(value=False)
        ttk.Checkbutton(opts, text="Dry Run (no changes)", variable=self.dry_run).grid(row=0, column=0, sticky="w")
        ttk.Label(opts, text="Hint: On Windows, run as Administrator for installs.", foreground="#666").grid(row=0, column=1, sticky="e")

        actions = ttk.Frame(self, padding=10)
        actions.grid(row=3, column=0, sticky="ew")
        self.install_btn = ttk.Button(actions, text="Install Apps", command=self.install_apps)
        self.install_btn.pack(side="left")
        self.make_dirs_btn = ttk.Button(actions, text="Create Directories", command=self.create_directories)
        self.make_dirs_btn.pack(side="left", padx=6)
        self.stop_btn = ttk.Button(actions, text="Stop", command=self.request_stop, state="disabled")
        self.stop_btn.pack(side="left")

        progress = ttk.Frame(self, padding=(10, 0, 10, 0))
        progress.grid(row=4, column=0, sticky="ew")
        self.prog = ttk.Progressbar(progress, mode="indeterminate")
        self.prog.pack(fill="x")

        log_frame = ttk.LabelFrame(self, text="Logs", padding=8)
        log_frame.grid(row=5, column=0, sticky="nsew", padx=10, pady=(8, 10))
        self.log_text = tk.Text(log_frame, height=12, wrap="word")
        self.log_text.pack(fill="both", expand=True)
        self.log_text.configure(state="disabled")
        self.after(100, self._drain_log_queue)

        self.status = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status, anchor="w").grid(row=6, column=0, sticky="ew")

        # menu
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_config)
        file_menu.add_command(label="Open…", command=self.load_config_dialog)
        file_menu.add_command(label="Save", command=self.save_config, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As…", command=self.save_config_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        catalog_menu = tk.Menu(menubar, tearoff=0)
        catalog_menu.add_command(label="Load apps.info…", command=self._load_catalog_from_dialog)
        catalog_menu.add_command(label="Reload apps.info", command=self._load_catalog_auto)
        menubar.add_cascade(label="Catalog", menu=catalog_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo(APP_TITLE, "Dev Environment Booster\nCatalog picker + search\n50 Days • 50 Projects"))
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    # ---------- catalog ----------
    def _load_catalog_auto(self):
        # default path: same folder as this script
        here = os.path.dirname(os.path.abspath(__file__))
        fp = os.path.join(here, "apps.info")
        if os.path.exists(fp):
            self._load_catalog(fp)
        else:
            self.catalog = []
            self.catalog_loaded = False
            self._refresh_catalog_list()
            self._log("No apps.info found (place it next to gui).")

    def _load_catalog_from_dialog(self):
        fp = filedialog.askopenfilename(
            title="Open apps.info",
            filetypes=[("JSON files", "*.json;*.JSON;*.info"), ("All files", "*.*")]
        )
        if fp:
            self._load_catalog(fp)

    def _load_catalog(self, fp):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("apps.info must be a JSON array of {id,name,category}")
            self.catalog = data
            self.catalog_loaded = True
            self._refresh_catalog_list()
            self._log(f"Loaded catalog: {fp} ({len(self.catalog)} entries)")
        except Exception as e:
            self.catalog_loaded = False
            self.catalog = []
            self._refresh_catalog_list()
            messagebox.showerror("Catalog Error", f"Failed to load apps.info:\n{e}")

    def _refresh_catalog_list(self):
        query = self.search_var.get().strip().lower()
        self.catalog_list.delete(0, "end")
        if not self.catalog:
            self.catalog_list.insert("end", "— No catalog loaded —")
            return
        for item in self.catalog:
            name = (item.get("name") or "").lower()
            app_id = (item.get("id") or "").lower()
            cat = (item.get("category") or "").lower()
            if query and (query not in name and query not in app_id and query not in cat):
                continue
            display = f"{item.get('name','?')}  —  {item.get('id','?')}  [{item.get('category','misc')}]"
            self.catalog_list.insert("end", display)

    def add_from_catalog_double(self):
        sel = self.catalog_list.curselection()
        if not sel:
            return
        self._add_catalog_item_by_index(sel[0])

    def add_from_catalog_selected(self):
        sel = self.catalog_list.curselection()
        if not sel:
            return
        for idx in sel:
            self._add_catalog_item_by_index(idx)

    def _add_catalog_item_by_index(self, idx):
        if not self.catalog:
            return
        # if the first line is the placeholder "— No catalog loaded —"
        if idx >= len(self.catalog):
            return
        item = self.catalog[idx]
        # append as {"id": ..., "name": ...}
        self.config_data.setdefault("apps", []).append({"id": item.get("id"), "name": item.get("name")})
        self._refresh_lists()
        self._mark_dirty()
        self._log(f"Added from catalog: {item.get('name')} ({item.get('id')})")

    # ---------- config I/O ----------
    def new_config(self):
        if not self._confirm_discard_if_dirty():
            return
        self.config_data = {"apps": [], "paths": []}
        self.current_config_path = None
        self.path_var.set("")
        self._refresh_lists()
        self._mark_clean()
        self._log("Started new config.")

    def load_config_dialog(self):
        fp = filedialog.askopenfilename(
            title="Open setup.JSON",
            filetypes=[("JSON files", "*.json;*.JSON"), ("All files", "*.*")]
        )
        if fp:
            self.load_config(fp)

    def load_config(self, fp):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                self.config_data = json.load(f)
            self.current_config_path = fp
            self.path_var.set(fp)
            self._refresh_lists()
            self._mark_clean()
            self._log(f"Loaded config from {fp}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON:\n{e}")

    def save_config(self, *_):
        if not self.current_config_path:
            return self.save_config_as()
        try:
            with open(self.current_config_path, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=2)
            self._mark_clean()
            self._log(f"Saved: {self.current_config_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON:\n{e}")

    def save_config_as(self, *_):
        fp = filedialog.asksaveasfilename(
            title="Save setup.JSON",
            defaultextension=".json",
            initialfile="setup.JSON",
            filetypes=[("JSON files", "*.json;*.JSON"), ("All files", "*.*")]
        )
        if not fp:
            return
        self.current_config_path = fp
        self.path_var.set(fp)
        self.save_config()

    # ---------- list management ----------
    def _refresh_lists(self):
        self.apps_list.delete(0, "end")
        for a in self.config_data.get("apps", []):
            label, app_id, app_name = normalize_app_entry(a)
            self.apps_list.insert("end", f"{label}  [{app_id or 'name'}]")
        self.paths_list.delete(0, "end")
        for p in self.config_data.get("paths", []):
            self.paths_list.insert("end", p)

    def add_app_by_name(self):
        name = self.new_app_var.get().strip()
        if not name:
            return
        self.config_data.setdefault("apps", []).append(name)
        self.new_app_var.set("")
        self._refresh_lists()
        self._mark_dirty()

    def add_app_by_id(self):
        app_id = self.new_app_var.get().strip()
        if not app_id:
            return
        self.config_data.setdefault("apps", []).append({"id": app_id, "name": app_id.split(".")[-1]})
        self.new_app_var.set("")
        self._refresh_lists()
        self._mark_dirty()

    def remove_selected_apps(self):
        sel = list(self.apps_list.curselection())[::-1]
        if not sel:
            return
        for idx in sel:
            del self.config_data["apps"][idx]
        self._refresh_lists()
        self._mark_dirty()

    def pick_folder_for_path(self):
        folder = filedialog.askdirectory(title="Choose directory")
        if folder:
            self.new_path_var.set(folder)

    def add_path(self):
        p = self.new_path_var.get().strip()
        if not p:
            return
        if p in self.config_data.setdefault("paths", []):
            messagebox.showinfo("Duplicate", f"'{p}' already exists.")
            return
        self.config_data["paths"].append(p)
        self.new_path_var.set("")
        self._refresh_lists()
        self._mark_dirty()

    def remove_selected_paths(self):
        sel = list(self.paths_list.curselection())[::-1]
        if not sel:
            return
        for idx in sel:
            del self.config_data["paths"][idx]
        self._refresh_lists()
        self._mark_dirty()

    # ---------- operations ----------
    def install_apps(self):
        if not self.config_data.get("apps"):
            messagebox.showwarning("No Apps", "No apps listed.")
            return
        if not self.pkg_mgr:
            messagebox.showwarning("No Package Manager", "No supported package manager detected.")
            return
        self._run_worker(self._install_worker, "Installing apps…")

    def create_directories(self):
        if not self.config_data.get("paths"):
            messagebox.showwarning("No Paths", "No directories listed.")
            return
        self._run_worker(self._mkdir_worker, "Creating directories…")

    def _run_worker(self, target, status_msg):
        if self.worker_thread and self.worker_thread.is_alive():
            messagebox.showinfo("Busy", "An operation is already running.")
            return
        self.stop_flag.clear()
        self._disable_controls(True)
        self.status.set(status_msg)
        self.worker_thread = threading.Thread(target=target, daemon=True)
        self.worker_thread.start()

    def request_stop(self):
        self.stop_flag.set()
        self._log("Stop requested…")

    def _install_worker(self):
        apps = self.config_data.get("apps", [])
        pkg_mgr = self.pkg_mgr
        dry = self.dry_run.get()
        ok = True

        for i, app in enumerate(apps, 1):
            if self.stop_flag.is_set():
                self._log("⏹️ Installation aborted by user.")
                ok = False
                break

            label, app_id, app_name = normalize_app_entry(app)

            # Pre-check
            installed = is_installed(pkg_mgr, app_id, app_name)
            if installed is True:
                self._log(f"✅ Already installed — skipped: {label}")
                continue

            cmd = build_install_cmd(pkg_mgr, app_id, app_name)
            if not cmd:
                self._log(f"⚠️ Unsupported package manager or bad entry: {label}")
                ok = False
                continue

            if dry:
                self._log(f"(DRY-RUN) Would install: {label} via {pkg_mgr} → {' '.join(cmd)}")
                continue

            self._log(f"📦 Installing ({i}/{len(apps)}): {label}")
            try:
                proc = run_cmd_capture(cmd, shell=(pkg_mgr == "winget"))
                out = (proc.stdout or "") + (proc.stderr or "")
                if proc.returncode == 0:
                    self._log(f"✅ Installed: {label}")
                else:
                    if pkg_mgr == "winget":
                        low = out.lower()
                        if "is already installed" in low or "no applicable update found" in low:
                            self._log(f"✅ Already installed — skipped: {label}")
                            continue
                        if is_ambiguous_winget(out):
                            hint = "Use an exact ID in JSON (e.g., {'id': 'Docker.DockerDesktop', 'name': 'docker'})."
                            self._log(f"❌ Ambiguous package name: '{label}'. {hint}")
                            ok = False
                            continue
                    self._log(f"❌ Failed: {label}\n{out.strip()}")
                    ok = False
            except Exception as e:
                self._log(f"❌ Error installing {label}: {e}")
                ok = False

        self._finish(ok)

    def _mkdir_worker(self):
        paths = self.config_data.get("paths", [])
        dry = self.dry_run.get()
        ok = True
        for i, p in enumerate(paths, 1):
            if self.stop_flag.is_set():
                self._log("⏹️ Directory creation aborted by user.")
                ok = False
                break
            try:
                if dry:
                    self._log(f"(DRY-RUN) Would create: {p}")
                else:
                    os.makedirs(p, exist_ok=True)
                    self._log(f"📁 Created/exists: {p}")
            except Exception as e:
                self._log(f"❌ Error creating {p}: {e}")
                ok = False
        self._finish(ok)

    # ---------- state/UX ----------
    def _disable_controls(self, busy=True):
        state = "disabled" if busy else "normal"
        for w in (self.install_btn, self.make_dirs_btn):
            w.config(state=state)
        self.stop_btn.config(state="normal" if busy else "disabled")
        (self.prog.start(10) if busy else self.prog.stop())

    def _finish(self, ok):
        self._disable_controls(False)
        self.status.set("Done" if ok else "Completed with errors")
        self._log("🎉 Completed successfully." if ok else "⚠️ Completed with some errors.")

    def _log(self, msg):
        self.log_queue.put(msg)

    def _drain_log_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_text.configure(state="normal")
                self.log_text.insert("end", msg + "\n")
                self.log_text.see("end")
                self.log_text.configure(state="disabled")
        except queue.Empty:
            pass
        self.after(120, self._drain_log_queue)

    def _mark_dirty(self):
        self.title(f"* {APP_TITLE}")
        self._dirty = True

    def _mark_clean(self):
        self.title(APP_TITLE)
        self._dirty = False

    def _confirm_discard_if_dirty(self):
        return True if not getattr(self, "_dirty", False) else messagebox.askyesno("Unsaved changes", "Discard unsaved changes?")

# ---------------- main ----------------
if __name__ == "__main__":
    app = BoosterGUI()
    app.mainloop()
