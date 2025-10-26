# Clipboard Logger — USAGE

## What it does
Clipboard Logger monitors the system clipboard in real time and records copy events. It logs:
- Text clipboard entries (saved into logs/logs.json and displayed in the GUI)
- Image clipboard entries (if Pillow is installed) — saved to logs/images/

This tool is intended for debugging and personal tracking. **Do not use it to capture sensitive data without consent.**

## Features
- Lightweight Tkinter GUI with start/stop monitoring
- Live feed of clipboard events with timestamps
- Save logs to JSON and optionally save images to disk
- Pause/resume monitoring
- Clear logs and export logs to CSV

## Requirements
- Python 3.8+
- Optional: Pillow (for image clipboard support) — `pip install pillow`
- Optional: pyperclip (for robust cross-platform text clipboard) — `pip install pyperclip`
  - If pyperclip is not available, Tkinter's clipboard will be used for text capture.
- On Linux, additional clipboard backends may be required (xclip/xsel).

## Safety & Privacy
- The logger stores clipboard contents locally under the `logs/` folder.
- Avoid running when handling passwords or sensitive personal data.

## Files
- `src/clipboard_logger.py` — main GUI app
- `docs/USAGE.md` — this file
- `README.md` — project readme
- `HowToRun.txt` — quick run steps
- `LICENSE` — MIT
