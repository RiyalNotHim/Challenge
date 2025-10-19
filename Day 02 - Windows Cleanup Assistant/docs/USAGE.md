# USAGE — Windows Cleanup Assistant

## What this project does
Windows Cleanup Assistant is a Python utility that provides a small graphical interface to perform common Windows cleanup tasks by invoking PowerShell commands. It helps free disk space by removing temporary files, system logs, caches, and other safe-to-remove items.

> NOTE: This tool runs commands that delete files. Review tasks before running and run as Administrator for the most effective cleanup.

## Features
- Remove user's temporary files (%%TEMP%%)
- Empty Recycle Bin
- Clear Windows Update cache (SoftwareDistribution\Download)
- Clear the thumbnail cache
- Clear DNS cache (ipconfig /flushdns)
- Optionally clear Chrome & Edge browser cache folders for the current user
- Simple tkinter GUI with a live log window
- Runs PowerShell commands; shows output, errors, and byte counts cleaned

## How it works
The Python GUI prepares and executes PowerShell commands using `subprocess`. Each cleanup task is executed separately and logged. The script attempts to run elevated commands where needed but does not implement an elevation prompt — run the script from an elevated prompt for full privileges.

## Safety
- The tool avoids touching user documents. It focuses on system and application caches known to be safe to remove.
- Browser cache clearing targets the default profile cache folders. Use with caution if you want to keep session state.
- Backup your system or important data if you're unsure.

## Files
- `src/win_cleanup_assistant.py` — main GUI script
- `docs/USAGE.md` — this file
- `HowToRun.txt` — quick run instructions
- `README.md` — project readme (copied from repo)
- `LICENSE` — MIT license

## Troubleshooting
- If some tasks fail due to permissions, run the script as Administrator.
- If PowerShell isn't found, ensure Windows PowerShell is installed and in PATH.
