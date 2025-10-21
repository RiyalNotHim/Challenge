
"""
Windows Cleanup Assistant
A small tkinter GUI that runs a set of PowerShell cleanup commands.

Author: Sattyam Chavan
"""
import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# ---------- Helpers ----------
def run_powershell(cmd):
    """
    Run a PowerShell command and return (returncode, stdout, stderr)
    """
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True, text=True, timeout=300
        )
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as e:
        return 1, "", str(e)

def log(msg, clear=False):
    if clear:
        LOG_WIDGET.configure(state="normal")
        LOG_WIDGET.delete(1.0, tk.END)
        LOG_WIDGET.configure(state="disabled")
    else:
        LOG_WIDGET.configure(state="normal")
        LOG_WIDGET.insert(tk.END, msg + "\n")
        LOG_WIDGET.see(tk.END)
        LOG_WIDGET.configure(state="disabled")

# ---------- Cleanup tasks ----------
def clean_temp_files():
    # user's temp folder
    temp = os.environ.get("TEMP") or os.environ.get("TMP")
    if not temp:
        return 1, "", "TEMP env var not found"
    cmd = f"Remove-Item -LiteralPath '{temp}\\*' -Recurse -Force -ErrorAction SilentlyContinue"
    return run_powershell(cmd)

def empty_recycle_bin():
    # Use .NET to empty recycle bin
    cmd = "[void][Windows.Storage.StorageApplicationPermissions,Windows.Foundation,ContentType=WindowsRuntime];" \
          " $shell = New-Object -ComObject Shell.Application; $recycle = $shell.Namespace(0xA); $recycle.Items() | ForEach-Object { $recycle.InvokeVerb('delete') }"
    # fallback: use Shell32 - but some environments might block
    return run_powershell(cmd)

def clear_windows_update_cache():
    # Stops wuauserv, deletes SoftwareDistribution\Download
    cmd = "Stop-Service -Name wuauserv -Force -ErrorAction SilentlyContinue; " \
          "Remove-Item -LiteralPath \"$env:windir\\SoftwareDistribution\\Download\\*\" -Recurse -Force -ErrorAction SilentlyContinue; " \
          "Start-Service -Name wuauserv -ErrorAction SilentlyContinue"
    return run_powershell(cmd)

def clear_thumbnail_cache():
    cmd = "Remove-Item -LiteralPath \"$env:LOCALAPPDATA\\Microsoft\\Windows\\Explorer\\thumbcache_*\" -Force -ErrorAction SilentlyContinue"
    return run_powershell(cmd)

def flush_dns():
    cmd = "ipconfig /flushdns"
    return run_powershell(cmd)

def clear_chrome_edge_cache():
    # Clear default cache folders for Chrome and Edge for the current user
    user = os.environ.get("USERPROFILE")
    cmds = []
    chrome = os.path.join(user or "", "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cache")
    edge = os.path.join(user or "", "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Cache")
    if os.path.exists(chrome):
        cmds.append(f"Remove-Item -LiteralPath '{chrome}\\*' -Recurse -Force -ErrorAction SilentlyContinue")
    if os.path.exists(edge):
        cmds.append(f"Remove-Item -LiteralPath '{edge}\\*' -Recurse -Force -ErrorAction SilentlyContinue")
    if not cmds:
        return 1, "", "No browser cache folders found"
    full = "; ".join(cmds)
    return run_powershell(full)

# ---------- GUI and threading ----------
def worker(tasks):
    log("Starting cleanup sequence...")
    total_cleaned = 0
    for name, func in tasks:
        log(f"--> Running: {name}")
        rc, out, err = func()
        if out:
            log(out.strip())
        if err:
            log("ERR: " + err.strip())
        log(f"--> Finished: {name} (rc={rc})")
    log("Cleanup sequence finished.")

def start_cleanup():
    selected = []
    if var_temp.get():
        selected.append(("Temp files", clean_temp_files))
    if var_recycle.get():
        selected.append(("Recycle Bin", empty_recycle_bin))
    if var_wu.get():
        selected.append(("Windows Update Cache", clear_windows_update_cache))
    if var_thumbs.get():
        selected.append(("Thumbnail Cache", clear_thumbnail_cache))
    if var_dns.get():
        selected.append(("Flush DNS", flush_dns))
    if var_browser.get():
        selected.append(("Browser Cache (Chrome/Edge)", clear_chrome_edge_cache))

    if not selected:
        messagebox.showinfo("Nothing selected", "Select at least one cleanup task.")
        return

    t = threading.Thread(target=worker, args=(selected,), daemon=True)
    t.start()

# ---------- Build GUI ----------
root = tk.Tk()
root.title("Windows Cleanup Assistant")
root.geometry("700x500")

frm = ttk.Frame(root, padding=10)
frm.pack(fill="both", expand=True)

lbl = ttk.Label(frm, text="Select cleanup tasks:", font=("Segoe UI", 12, "bold"))
lbl.pack(anchor="w", pady=(0,5))

var_temp = tk.BooleanVar(value=True)
var_recycle = tk.BooleanVar(value=False)
var_wu = tk.BooleanVar(value=True)
var_thumbs = tk.BooleanVar(value=True)
var_dns = tk.BooleanVar(value=True)
var_browser = tk.BooleanVar(value=False)

checks = [
    ("Clean user's temporary files (%%TEMP%%)", var_temp),
    ("Empty Recycle Bin (may not work in all environments)", var_recycle),
    ("Clear Windows Update download cache (SoftwareDistribution\\Download)", var_wu),
    ("Clear thumbnail cache", var_thumbs),
    ("Flush DNS cache (ipconfig /flushdns)", var_dns),
    ("Clear Chrome/Edge cache for current user (if present)", var_browser),
]

for text, var in checks:
    ttk.Checkbutton(frm, text=text, variable=var).pack(anchor="w", pady=2)

btn_frame = ttk.Frame(frm)
btn_frame.pack(fill="x", pady=10)

run_btn = ttk.Button(btn_frame, text="Run Cleanup", command=start_cleanup)
run_btn.pack(side="left")

clear_btn = ttk.Button(btn_frame, text="Clear Log", command=lambda: log("", clear=True))
clear_btn.pack(side="left", padx=8)

exit_btn = ttk.Button(btn_frame, text="Exit", command=root.destroy)
exit_btn.pack(side="right")

# Log area
LOG_WIDGET = scrolledtext.ScrolledText(frm, height=15, state="disabled")
LOG_WIDGET.pack(fill="both", expand=True, pady=(8,0))

root.mainloop()
