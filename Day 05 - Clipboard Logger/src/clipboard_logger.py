"""
Clipboard Logger GUI
Monitors the clipboard for text and images and logs entries to data/clipboard_log.json.
Optional image support (requires Pillow).
"""
import os
import json
import threading
import time
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText

# Optional Pillow for image clipboard support
try:
    from PIL import Image, ImageTk, ImageGrab
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
LOG_FILE = DATA_DIR / "clipboard_log.json"
IMAGES_DIR = DATA_DIR / "images"

POLL_INTERVAL = 0.7  # seconds


def ensure_storage():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        with LOG_FILE.open("w", encoding="utf-8") as f:
            json.dump({"entries": []}, f, indent=2)


def load_log():
    ensure_storage()
    with LOG_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_log(log):
    ensure_storage()
    with LOG_FILE.open("w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)


def timestamp():
    return datetime.now().isoformat()


class ClipboardMonitor(threading.Thread):
    def __init__(self, callback):
        super().__init__(daemon=True)
        self.callback = callback
        self._running = True
        self._paused = False
        self._last_text = None
        self._last_image_id = None

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            if self._paused:
                time.sleep(POLL_INTERVAL)
                continue

            # Check for text
            text = None
            try:
                root = tk.Tk()
                root.withdraw()
                text = root.clipboard_get()
                root.destroy()
            except Exception:
                text = None

            if text and text != self._last_text:
                self._last_text = text
                entry = {"type": "text", "value": text, "ts": timestamp()}
                self.callback(entry)

            # Check for image via PIL.ImageGrab (optional)
            if PIL_AVAILABLE:
                try:
                    img = ImageGrab.grabclipboard()
                    if img is not None:
                        try:
                            from io import BytesIO
                            b = BytesIO()
                            img.save(b, format="PNG")
                            img_bytes = b.getvalue()
                            img_id = str(len(img_bytes)) + "-" + str(img.size)
                        except Exception:
                            img_id = str(time.time())

                        if img_id != self._last_image_id:
                            self._last_image_id = img_id
                            fname = f"img_{int(time.time())}.png"
                            path = IMAGES_DIR / fname
                            try:
                                img.save(path)
                                entry = {"type": "image", "file": str(path.name), "ts": timestamp()}
                                self.callback(entry)
                            except Exception:
                                pass
                except Exception:
                    pass

            time.sleep(POLL_INTERVAL)


class ClipboardGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clipboard Logger")
        self.geometry("900x600")
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        ensure_storage()
        self.log = load_log()

        self.monitor = ClipboardMonitor(self.on_new_entry)
        self.monitor.start()

        # Top controls
        ctrl_frame = ttk.Frame(self, padding=8)
        ctrl_frame.pack(side="top", fill="x")
        self.btn_pause = ttk.Button(ctrl_frame, text="Pause", command=self.toggle_pause)
        self.btn_pause.pack(side="left", padx=4)
        ttk.Button(ctrl_frame, text="Export JSON", command=self.export_json).pack(side="left", padx=4)
        ttk.Button(ctrl_frame, text="Clear Log", command=self.clear_log).pack(side="left", padx=4)
        ttk.Button(ctrl_frame, text="Open Data Folder", command=self.open_data_folder).pack(side="left", padx=4)
        ttk.Button(ctrl_frame, text="Quit", command=self.on_quit).pack(side="right", padx=4)

        # Middle layout
        middle = ttk.Frame(self)
        middle.pack(fill="both", expand=True, padx=8, pady=6)

        left = ttk.Frame(middle)
        left.pack(side="left", fill="y", padx=(0, 8))
        ttk.Label(left, text="History").pack(anchor="w")
        self.lst = tk.Listbox(left, width=40, height=25)
        self.lst.pack(fill="y", expand=False)
        self.lst.bind("<<ListboxSelect>>", self.on_select)

        right = ttk.Frame(middle)
        right.pack(side="right", fill="both", expand=True)
        ttk.Label(right, text="Preview").pack(anchor="w")
        self.preview = ScrolledText(right, wrap="word", height=20, state="disabled")
        self.preview.pack(fill="both", expand=True)
        self.img_label = ttk.Label(right)
        self.img_label.pack()

        self.reload_list()

    def on_new_entry(self, entry):
        self.log.setdefault("entries", []).insert(0, entry)
        save_log(self.log)
        try:
            self.after(0, self.reload_list)
        except Exception:
            pass

    def reload_list(self):
        self.lst.delete(0, "end")
        for e in self.log.get("entries", []):
            ts = e.get("ts", "")
            typ = e.get("type")
            label = f"[{ts}] {typ}"
            if typ == "text":
                snippet = e.get("value", "")[:60].replace("\n", " ")
                label += f": {snippet}"
            elif typ == "image":
                label += f": {e.get('file')}"
            self.lst.insert("end", label)

    def on_select(self, event=None):
        sel = self.lst.curselection()
        if not sel:
            return
        idx = sel[0]
        entry = self.log.get("entries", [])[idx]
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.img_label.configure(image="")
        if entry.get("type") == "text":
            self.preview.insert("end", entry.get("value", ""))
        elif entry.get("type") == "image":
            if PIL_AVAILABLE:
                try:
                    img_path = IMAGES_DIR / entry.get("file")
                    img = Image.open(img_path)
                    img.thumbnail((400, 400))
                    self.photo = ImageTk.PhotoImage(img)
                    self.img_label.configure(image=self.photo)
                except Exception as e:
                    self.preview.insert("end", f"Image: {entry.get('file')} (failed to load)\n{e}")
            else:
                self.preview.insert("end", f"Image: {entry.get('file')} (Pillow not installed)")
        self.preview.configure(state="disabled")

    def toggle_pause(self):
        if self.monitor._paused:
            self.monitor.resume()
            self.btn_pause.config(text="Pause")
        else:
            self.monitor.pause()
            self.btn_pause.config(text="Resume")

    def export_json(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"clipboard_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.log, f, indent=2)
        messagebox.showinfo("Exported", f"Exported log to {path}")

    def clear_log(self):
        if not messagebox.askyesno("Clear Log", "Delete all clipboard log entries?"):
            return
        self.log = {"entries": []}
        save_log(self.log)
        self.reload_list()
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.configure(state="disabled")
        self.img_label.configure(image="")

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

    def on_quit(self):
        if messagebox.askokcancel("Quit", "Exit Clipboard Logger?"):
            try:
                self.monitor.stop()
            except Exception:
                pass
            self.destroy()


def main():
    ensure_storage()
    app = ClipboardGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
