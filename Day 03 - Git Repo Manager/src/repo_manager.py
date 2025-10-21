"""
GitHub Repo Manager — Single Window Layout
Divided into: Run Tasks (left) | Summary (right) | Logs (bottom)
"""
import os
import sys
import json
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
from pathlib import Path

# ---------------- Utility Functions ----------------
def run_cmd(cmd, cwd=None):
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def safe_mkdir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def clone_repo(entry):
    url = entry["url"]
    path = entry["path"]
    safe_mkdir(os.path.dirname(path) or ".")
    cmd = ["git", "clone", url, path]
    if entry.get("branch"):
        cmd = ["git", "clone", "-b", entry["branch"], url, path]
    return run_cmd(cmd)

def pull_repo(entry):
    path = entry["path"]
    branch = entry.get("branch")
    if not os.path.exists(path):
        return 2, "", f"Path not found: {path}"
    run_cmd(["git", "fetch", "--all"], cwd=path)
    if branch:
        run_cmd(["git", "checkout", branch], cwd=path)
    return run_cmd(["git", "pull"], cwd=path)

# ---------------- GUI Class ----------------
class RepoManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Repo Manager")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)

        self.stats = {"total": 0, "success": 0, "failed": 0, "skipped": 0}
        self.json_path = tk.StringVar()

        # ---- Top Frame (Run + Summary) ----
        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(fill="both", expand=False)

        # Left side (Run Tasks)
        run_frame = ttk.LabelFrame(top_frame, text="Run Tasks", padding=10)
        run_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        ttk.Label(run_frame, text="Select JSON File:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ttk.Entry(run_frame, textvariable=self.json_path).pack(fill="x", pady=5)
        ttk.Button(run_frame, text="Browse", command=self.browse_json).pack(anchor="e", pady=3)

        self.progress = ttk.Progressbar(run_frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=8)

        btn_frame = ttk.Frame(run_frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Run", command=self.run_tasks).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Logs", command=self.clear_logs).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exit", command=self.root.destroy).pack(side="right", padx=5)

        self.status_label = ttk.Label(run_frame, text="Ready.", font=("Segoe UI", 9))
        self.status_label.pack(anchor="w", pady=(5, 0))

        # Right side (Summary)
        summary_frame = ttk.LabelFrame(top_frame, text="Summary", padding=10)
        summary_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        self.summary_box = tk.Text(summary_frame, height=8, wrap="word", state="disabled", font=("Segoe UI", 10))
        self.summary_box.pack(fill="both", expand=True)
        self.update_summary()

        # ---- Bottom Frame (Logs) ----
        log_frame = ttk.LabelFrame(root, text="Logs", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.log_box = scrolledtext.ScrolledText(log_frame, height=15, wrap="word", state="disabled", font=("Consolas", 10))
        self.log_box.pack(fill="both", expand=True)

    # ----------- UI Helpers -----------
    def browse_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if path:
            self.json_path.set(path)

    def log(self, msg, color="black"):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n", ("color",))
        self.log_box.tag_config("color", foreground=color)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def clear_logs(self):
        self.log_box.configure(state="normal")
        self.log_box.delete(1.0, "end")
        self.log_box.configure(state="disabled")

    def update_summary(self):
        self.summary_box.configure(state="normal")
        self.summary_box.delete(1.0, "end")
        summary = (
            f"Total Repositories: {self.stats['total']}\n"
            f"✅ Success: {self.stats['success']}\n"
            f"❌ Failed: {self.stats['failed']}\n"
            f"⚪ Skipped: {self.stats['skipped']}\n"
        )
        self.summary_box.insert("end", summary)
        self.summary_box.configure(state="disabled")

    # ----------- Task Processing -----------
    def run_tasks(self):
        json_path = self.json_path.get().strip()
        if not json_path or not os.path.exists(json_path):
            messagebox.showerror("Error", "Please select a valid JSON file.")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.stats = {"total": len(data), "success": 0, "failed": 0, "skipped": 0}
        self.progress["maximum"] = len(data)
        self.progress["value"] = 0
        self.clear_logs()
        self.update_summary()
        self.status_label.config(text="Running tasks...")

        threading.Thread(target=self._process_repos, args=(data,), daemon=True).start()

    def _process_repos(self, data):
        for i, entry in enumerate(data):
            name = entry.get("name") or entry.get("url")
            self.log(f"[{i+1}/{len(data)}] Processing {name}...", color="blue")

            if entry.get("skip"):
                self.log(f"⚪ Skipped {name}", color="gray")
                self.stats["skipped"] += 1
            elif not os.path.exists(entry["path"]) or not os.path.isdir(os.path.join(entry["path"], ".git")):
                rc, out, err = clone_repo(entry)
                if rc == 0:
                    self.log(f"✅ Cloned {name}", color="green")
                    self.stats["success"] += 1
                else:
                    self.log(f"❌ Clone failed for {name}: {err}", color="red")
                    self.stats["failed"] += 1
            else:
                rc, out, err = pull_repo(entry)
                if rc == 0:
                    self.log(f"🔄 Pulled updates for {name}", color="green")
                    self.stats["success"] += 1
                else:
                    self.log(f"❌ Pull failed for {name}: {err}", color="red")
                    self.stats["failed"] += 1

            self.progress["value"] = i + 1
            self.update_summary()
            self.root.update_idletasks()

        self.status_label.config(text="All tasks completed.")
        messagebox.showinfo("Done", "All repositories processed successfully.")

# ---------------- Run App ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = RepoManagerApp(root)
    root.mainloop()
