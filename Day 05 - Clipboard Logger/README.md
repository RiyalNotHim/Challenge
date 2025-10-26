# Clipboard Logger 🖱️📋
> Monitors clipboard activity (text & images) and logs copy events in real time.

This lightweight tool provides a simple Tkinter GUI to start/stop clipboard monitoring, view captured entries, preview text and images, and export logs. It stores logs under `logs/` and saves clipboard images if Pillow is available.

**Warning:** Do not use to capture sensitive information without consent.

## Features
- Real-time monitoring of clipboard for text (pyperclip or Tkinter) and images (Pillow)
- GUI controls to start/stop monitoring, clear logs, export CSV, open logs folder
- Saves logs to `logs/logs.json` and images to `logs/images/`
- Cross-platform (best on Windows/macOS for image capture)

## Requirements
- Python 3.8+
- Optional: `pyperclip` and `Pillow` for better compatibility and image support

## Quick Start
1. Unzip the project.
2. (Optional) Install dependencies:
   ```bash
   pip install pyperclip pillow
   ```
3. Run the GUI:
   ```bash
   python src/clipboard_logger.py
   ```

## Files
- `src/clipboard_logger.py` — main GUI application
- `docs/USAGE.md` — usage guide
- `HowToRun.txt` — quick instructions
- `LICENSE` — MIT license
