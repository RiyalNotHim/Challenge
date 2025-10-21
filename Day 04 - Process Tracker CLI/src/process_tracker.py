
"""
Process Tracker GUI
A simple Tkinter GUI for the Process Tracker CLI's data model.
Reads/writes `data/tasks.json` in the same folder and keeps compatibility
with the CLI tool. Features:
- List tasks in a table
- Add task dialog
- Start / Stop timers
- Mark complete / Reopen
- Delete task
- Live running timer display
- Exports are still available via CLI script if needed
"""
import os
import json
import threading
from pathlib import Path
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog

# Constants
BASE_DIR = Path(__file__).resolve().parents[1] if (Path(__file__).resolve().parents and Path(__file__).exists()) else Path(".")
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "tasks.json"
LOCK = threading.Lock()
UI_REFRESH_MS = 1000  # update UI every second

# Utilities for data handling
def ensure_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump({"next_id": 1, "tasks": []}, f, indent=2)

def load_data():
    ensure_data()
    with LOCK:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)

def save_data(d):
    ensure_data()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = DATA_DIR / f"tasks_backup_{ts}.json"
    with LOCK:
        # create backup
        try:
            with DATA_FILE.open("r", encoding="utf-8") as f:
                old = f.read()
            with backup.open("w", encoding="utf-8") as bf:
                bf.write(old)
        except Exception:
            # ignore if backup fails (e.g., file missing)
            pass
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)

# Time helpers
def iso_now():
    return datetime.now().isoformat()

def parse_iso(s):
    try:
        return datetime.fromisoformat(s)
    except Exception:
        # fallback naive parse
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")

def minutes_between(a_iso, b_iso):
    a = parse_iso(a_iso)
    b = parse_iso(b_iso)
    return int((b - a).total_seconds() / 60)

def human_delta_minutes(minutes):
    # return H:MM string
    h = minutes // 60
    m = minutes % 60
    if h:
        return f"{h}h {m}m"
    return f"{m}m"

# Core operations (same semantics as CLI)
def add_task(title, description="", tags=None, estimate_minutes=None):
    d = load_data()
    tid = d.get("next_id", 1)
    task = {
        "id": tid,
        "title": title,
        "description": description,
        "tags": tags or [],
        "estimate_minutes": estimate_minutes,
        "created_at": iso_now(),
        "completed": False,
        "sessions": [],
        "running": None
    }
    d.setdefault("tasks", []).append(task)
    d["next_id"] = tid + 1
    save_data(d)
    return task

def start_task(tid):
    d = load_data()
    # stop any running tasks first
    for t in d.get("tasks", []):
        if t.get("running"):
            stop_task(t["id"], save=False)
    task = next((t for t in d.get("tasks", []) if t["id"] == tid), None)
    if not task:
        raise ValueError("Task not found")
    if task.get("running"):
        return False
    task["running"] = iso_now()
    save_data(d)
    return True

def stop_task(tid=None, save=True):
    d = load_data()
    if tid is None:
        task = next((t for t in d.get("tasks", []) if t.get("running")), None)
    else:
        task = next((t for t in d.get("tasks", []) if t["id"] == tid), None)
    if not task or not task.get("running"):
        return None
    start = task["running"]
    end = iso_now()
    minutes = minutes_between(start, end)
    session = {"start": start, "end": end, "minutes": minutes}
    task.setdefault("sessions", []).append(session)
    task["running"] = None
    if save:
        save_data(d)
    return session

def mark_done(tid):
    d = load_data()
    task = next((t for t in d.get("tasks", []) if t["id"] == tid), None)
    if not task:
        raise ValueError("Task not found")
    task["completed"] = True
    # if running, stop it
    if task.get("running"):
        stop_task(tid)
    save_data(d)

def reopen_task(tid):
    d = load_data()
    task = next((t for t in d.get("tasks", []) if t["id"] == tid), None)
    if not task:
        raise ValueError("Task not found")
    task["completed"] = False
    save_data(d)

def delete_task(tid):
    d = load_data()
    tasks = d.get("tasks", [])
    idx = next((i for i, t in enumerate(tasks) if t["id"] == tid), None)
    if idx is None:
        raise ValueError("Task not found")
    tasks.pop(idx)
    save_data(d)

def log_manual(tid, minutes):
    d = load_data()
    task = next((t for t in d.get("tasks", []) if t["id"] == tid), None)
    if not task:
        raise ValueError("Task not found")
    now = iso_now()
    session = {"start": now, "end": now, "minutes": minutes, "manual": True}
    task.setdefault("sessions", []).append(session)
    save_data(d)

# GUI Implementation
class ProcessTrackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Process Tracker")
        self.geometry("1000x650")
        self.resizable(False, False)

        # Top: Controls and stats
        top_frame = ttk.Frame(self, padding=(10, 8))
        top_frame.pack(side="top", fill="x")

        controls_frame = ttk.LabelFrame(top_frame, text="Controls", padding=8)
        controls_frame.pack(side="left", fill="x", expand=True)

        ttk.Button(controls_frame, text="Add Task", command=self.ui_add_task).pack(side="left", padx=6)
        ttk.Button(controls_frame, text="Start", command=self.ui_start_selected).pack(side="left", padx=6)
        ttk.Button(controls_frame, text="Stop", command=self.ui_stop_selected).pack(side="left", padx=6)
        ttk.Button(controls_frame, text="Mark Done", command=self.ui_mark_done).pack(side="left", padx=6)
        ttk.Button(controls_frame, text="Reopen", command=self.ui_reopen).pack(side="left", padx=6)
        ttk.Button(controls_frame, text="Delete", command=self.ui_delete).pack(side="left", padx=6)
        ttk.Button(controls_frame, text="Manual Log", command=self.ui_manual_log).pack(side="left", padx=6)
        ttk.Button(controls_frame, text="Export CSV", command=self.ui_export_csv).pack(side="left", padx=6)

        # Stats frame
        stats_frame = ttk.LabelFrame(top_frame, text="Stats", padding=8)
        stats_frame.pack(side="right", fill="y")

        self.lbl_total = ttk.Label(stats_frame, text="Total: 0")
        self.lbl_total.pack(anchor="w")
        self.lbl_active = ttk.Label(stats_frame, text="Active: 0")
        self.lbl_active.pack(anchor="w")
        self.lbl_completed = ttk.Label(stats_frame, text="Completed: 0")
        self.lbl_completed.pack(anchor="w")
        self.lbl_running = ttk.Label(stats_frame, text="Currently Running: -")
        self.lbl_running.pack(anchor="w")

        # Middle: Treeview table
        table_frame = ttk.Frame(self, padding=(10, 2))
        table_frame.pack(fill="both", expand=False)

        columns = ("id", "title", "est", "time_spent", "status", "running_since", "tags")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("est", text="Est (min)")
        self.tree.heading("time_spent", text="Time Spent")
        self.tree.heading("status", text="Status")
        self.tree.heading("running_since", text="Running Since")
        self.tree.heading("tags", text="Tags")
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("title", width=360, anchor="w")
        self.tree.column("est", width=80, anchor="center")
        self.tree.column("time_spent", width=100, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        self.tree.column("running_since", width=140, anchor="center")
        self.tree.column("tags", width=150, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Bottom: details & sessions
        bottom_frame = ttk.LabelFrame(self, text="Task Details & Sessions", padding=8)
        bottom_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=(8,10))

        # Left pane: details
        details_frame = ttk.Frame(bottom_frame)
        details_frame.pack(side="left", fill="both", expand=True)

        self.details_text = tk.Text(details_frame, wrap="word", height=10, state="disabled", font=("Segoe UI", 10))
        self.details_text.pack(fill="both", expand=True)

        # Right pane: buttons and quick actions
        right_actions = ttk.Frame(bottom_frame)
        right_actions.pack(side="right", fill="y")

        ttk.Button(right_actions, text="Refresh", command=self.refresh).pack(fill="x", pady=4)
        ttk.Button(right_actions, text="Open Data Folder", command=self.open_data_folder).pack(fill="x", pady=4)
        ttk.Button(right_actions, text="Quit", command=self.quit).pack(fill="x", pady=4)

        # Bind selection
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Start periodic UI refresh
        self.refresh()
        self.after(UI_REFRESH_MS, self._periodic_refresh)

    # ---------------- UI Actions ----------------
    def ui_add_task(self):
        dialog = AddTaskDialog(self)
        self.wait_window(dialog)
        if dialog.result:
            title, desc, tags, estimate = dialog.result
            add_task(title, desc, tags, estimate)
            self.refresh()
            messagebox.showinfo("Task Added", f"Added task: {title}")

    def ui_start_selected(self):
        sel = self.get_selected_task_id()
        if sel is None:
            messagebox.showwarning("No selection", "Select a task first.")
            return
        try:
            started = start_task(sel)
            if started:
                self.refresh()
            else:
                messagebox.showinfo("Already running", "Selected task is already running.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_stop_selected(self):
        sel = self.get_selected_task_id()
        try:
            if sel is None:
                # stop any running
                res = stop_task()
                if res is None:
                    messagebox.showinfo("No running task", "There is no running task.")
                else:
                    self.refresh()
                    messagebox.showinfo("Stopped", f"Stopped session: +{res['minutes']} minutes")
                return
            res = stop_task(sel)
            if res is None:
                messagebox.showinfo("Not running", "Selected task is not running.")
            else:
                self.refresh()
                messagebox.showinfo("Stopped", f"Stopped session: +{res['minutes']} minutes")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_mark_done(self):
        sel = self.get_selected_task_id()
        if sel is None:
            messagebox.showwarning("No selection", "Select a task first.")
            return
        try:
            mark_done(sel)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_reopen(self):
        sel = self.get_selected_task_id()
        if sel is None:
            messagebox.showwarning("No selection", "Select a task first.")
            return
        try:
            reopen_task(sel)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_delete(self):
        sel = self.get_selected_task_id()
        if sel is None:
            messagebox.showwarning("No selection", "Select a task first.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Delete task #{sel}? This action cannot be undone."):
            return
        try:
            delete_task(sel)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_manual_log(self):
        sel = self.get_selected_task_id()
        if sel is None:
            messagebox.showwarning("No selection", "Select a task first.")
            return
        val = simpledialog.askinteger("Manual Log", "Minutes to log:", minvalue=1, maxvalue=10000)
        if val is None:
            return
        try:
            log_manual(sel, val)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_export_csv(self):
        d = load_data()
        default = f"timesheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=default, filetypes=[("CSV files","*.csv")])
        if not path:
            return
        import csv
        rows = []
        for t in d.get("tasks", []):
            for s in t.get("sessions", []):
                rows.append({
                    "task_id": t["id"],
                    "title": t["title"],
                    "start": s.get("start"),
                    "end": s.get("end"),
                    "minutes": s.get("minutes", 0)
                })
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["task_id","title","start","end","minutes"])
                writer.writeheader()
                writer.writerows(rows)
            messagebox.showinfo("Exported", f"Exported {len(rows)} rows to {path}")
        except Exception as e:
            messagebox.showerror("Error exporting", str(e))

    def open_data_folder(self):
        try:
            path = str(DATA_DIR.resolve())
            if os.name == "nt":
                os.startfile(path)
            elif os.name == "posix":
                import subprocess
                subprocess.Popen(["xdg-open", path])
            else:
                messagebox.showinfo("Data Folder", path)
        except Exception:
            messagebox.showinfo("Data Folder", str(DATA_DIR))

    # ---------------- Helpers ----------------
    def get_selected_task_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        item = sel[0]
        try:
            return int(self.tree.set(item, "id"))
        except Exception:
            return None

    def on_select(self, event=None):
        tid = self.get_selected_task_id()
        if tid is None:
            self.details_text.configure(state="normal")
            self.details_text.delete("1.0", "end")
            self.details_text.configure(state="disabled")
            return
        d = load_data()
        task = next((t for t in d.get("tasks", []) if t["id"] == tid), None)
        if not task:
            return
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")
        self.details_text.insert("end", f"Task #{task['id']}: {task['title']}\n")
        self.details_text.insert("end", f"Description: {task.get('description') or ''}\n")
        self.details_text.insert("end", f"Tags: {', '.join(task.get('tags') or [])}\n")
        self.details_text.insert("end", f"Estimate (min): {task.get('estimate_minutes') or ''}\n")
        total = sum(s.get("minutes", 0) for s in task.get("sessions", []))
        self.details_text.insert("end", f"Total time tracked: {total} minutes ({human_delta_minutes(total)})\n")
        self.details_text.insert("end", f"Completed: {'Yes' if task.get('completed') else 'No'}\n")
        self.details_text.insert("end", f"Running: {task.get('running') or 'No'}\n\n")
        self.details_text.insert("end", "Sessions:\n")
        for s in task.get("sessions", []):
            mark = " (manual)" if s.get("manual") else ""
            self.details_text.insert("end", f" - {s.get('start')} → {s.get('end')} : {s.get('minutes')} min{mark}\n")
        self.details_text.configure(state="disabled")

    def refresh(self):
        # Reload data and refresh tree and stats
        d = load_data()
        tasks = sorted(d.get("tasks", []), key=lambda x: x["id"])
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        total = len(tasks)
        active = sum(1 for t in tasks if not t.get("completed"))
        completed = sum(1 for t in tasks if t.get("completed"))
        running_task = next((t for t in tasks if t.get("running")), None)
        running_label = f"#{running_task['id']} - {running_task['title']}" if running_task else "-"
        self.lbl_total.config(text=f"Total: {total}")
        self.lbl_active.config(text=f"Active: {active}")
        self.lbl_completed.config(text=f"Completed: {completed}")
        self.lbl_running.config(text=f"Currently Running: {running_label}")

        for t in tasks:
            total_minutes = sum(s.get("minutes", 0) for s in t.get("sessions", []))
            running_since = t.get("running") or ""
            status = "Done" if t.get("completed") else ("Running" if t.get("running") else "Open")
            tags = ", ".join(t.get("tags") or [])
            est = t.get("estimate_minutes") or ""
            # show human readable time spent
            time_spent = human_delta_minutes(total_minutes)
            self.tree.insert("", "end", values=(t["id"], t["title"], est, time_spent, status, running_since, tags))

        # Update details if selection exists
        self.on_select()

    def _periodic_refresh(self):
        # Update running timer display & tree periodically
        # We will update time_spent for running task(s) in the tree
        d = load_data()
        tasks = {t["id"]: t for t in d.get("tasks", [])}
        for item in self.tree.get_children():
            try:
                tid = int(self.tree.set(item, "id"))
            except Exception:
                continue
            t = tasks.get(tid)
            if not t:
                continue
            total_minutes = sum(s.get("minutes", 0) for s in t.get("sessions", []))
            if t.get("running"):
                try:
                    # calculate current extra minutes since running start
                    start = parse_iso(t["running"])
                    extra = int((datetime.now() - start).total_seconds() / 60)
                    display_minutes = total_minutes + extra
                except Exception:
                    display_minutes = total_minutes
                time_spent = human_delta_minutes(display_minutes)
                running_since = t.get("running")
                status = "Running"
            else:
                time_spent = human_delta_minutes(total_minutes)
                running_since = ""
                status = "Done" if t.get("completed") else "Open"
            # update tree row
            self.tree.set(item, "time_spent", time_spent)
            self.tree.set(item, "running_since", running_since)
            self.tree.set(item, "status", status)
        # update stats and details
        self.refresh_stats_labels()
        self.after(UI_REFRESH_MS, self._periodic_refresh)

    def refresh_stats_labels(self):
        d = load_data()
        tasks = d.get("tasks", [])
        total = len(tasks)
        active = sum(1 for t in tasks if not t.get("completed"))
        completed = sum(1 for t in tasks if t.get("completed"))
        running_task = next((t for t in tasks if t.get("running")), None)
        running_label = f"#{running_task['id']} - {running_task['title']}" if running_task else "-"
        self.lbl_total.config(text=f"Total: {total}")
        self.lbl_active.config(text=f"Active: {active}")
        self.lbl_completed.config(text=f"Completed: {completed}")
        self.lbl_running.config(text=f"Currently Running: {running_label}")

# Simple dialog to add task
class AddTaskDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Task")
        self.geometry("420x300")
        self.resizable(False, False)
        self.result = None

        ttk.Label(self, text="Title:").pack(anchor="w", padx=10, pady=(10,0))
        self.entry_title = ttk.Entry(self)
        self.entry_title.pack(fill="x", padx=10)

        ttk.Label(self, text="Description:").pack(anchor="w", padx=10, pady=(8,0))
        self.entry_desc = tk.Text(self, height=6)
        self.entry_desc.pack(fill="both", padx=10)

        tags_frame = ttk.Frame(self)
        tags_frame.pack(fill="x", padx=10, pady=6)
        ttk.Label(tags_frame, text="Tags (comma separated):").pack(side="left")
        self.entry_tags = ttk.Entry(tags_frame)
        self.entry_tags.pack(side="left", fill="x", expand=True, padx=(6,0))

        est_frame = ttk.Frame(self)
        est_frame.pack(fill="x", padx=10)
        ttk.Label(est_frame, text="Estimate (minutes):").pack(side="left")
        self.entry_est = ttk.Entry(est_frame, width=8)
        self.entry_est.pack(side="left", padx=(6,0))

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="Add", command=self.on_add).pack(side="right", padx=8)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="right")

    def on_add(self):
        title = self.entry_title.get().strip()
        if not title:
            messagebox.showwarning("Validation", "Title is required.")
            return
        desc = self.entry_desc.get("1.0", "end").strip()
        tags = [t.strip() for t in self.entry_tags.get().split(",") if t.strip()]
        est = self.entry_est.get().strip()
        estimate = int(est) if est.isdigit() else None
        self.result = (title, desc, tags, estimate)
        self.destroy()

# Entry point
def main():
    ensure_data()
    app = ProcessTrackerGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
