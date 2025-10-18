# 🧭 Dev Environment Booster (GUI) — Usage & Technical Guide

> **Project Day:** 01 — Dev Environment Booster  
> **App Name:** `gui_setup_booster.py`  
> **Purpose:** Automate dev machine setup (install apps + create directories) with a simple GUI, JSON configs, and a searchable app catalog.

---

## 1) What This App Does

This GUI tool helps you quickly set up a fresh development environment by:
- Reading a **config JSON** with two lists:
  - `apps`: tools to install (using **winget**, **apt**, **dnf**, **pacman**, or **brew**)
  - `paths`: folders to create (e.g., `C:/Projects`)
- Providing a **GUI** to:
  - **Add/Remove** apps and paths
  - **Open/Save** JSON configs (`setup.JSON`)
  - **Search & pick** from a local **apps catalog** (`apps.info`) and add to config with double-click
  - **Dry Run** actions to preview
  - Run **Install Apps** or **Create Directories** with live logs

---

## 2) Supported Platforms & Package Managers

- **Windows:** `winget` (preferred)
- **Linux:** `apt`, `dnf`, or `pacman` (auto-detected)
- **macOS:** `brew` (Homebrew)

> The app auto-detects the available package manager. If none is found, it will disable the install feature.

---

## 3) Files & Structure

```
📁 Day 01 - Dev Environment Booster
 ┣ 📂 docs/
 ┃ ┗ 📄 USAGE.md        ← this file
 ┣ 📂 src/
 ┃ ┣ 📄 gui_setup_booster.py  ← the GUI app
 ┃ ┣ 📄 setup.JSON            ← your working config (open/save in the app)
 ┃ ┗ 📄 apps.info             ← optional catalog (JSON array of {id, name, category})
 ┣ 📄 HowToRun.txt
 ┣ 📄 LICENSE
 ┗ 📄 README.md
```

---

## 4) Dependencies (Python Standard Library Only)

This app uses only **Python’s standard library** (no pip install needed):

- `tkinter` — GUI toolkit
- `json` — read/write configuration and catalog files
- `os`, `platform` — filesystem, OS detection
- `subprocess` — run package manager commands
- `threading` — background execution
- `queue` — thread-safe logs
- `shutil.which` — check available managers

---

## 5) Configuration Files

See README.md for full setup and example.

---

## 6) How to Run

```bash
cd src
python gui_setup_booster.py
```

---

## 7) Permissions & Security

- **Windows:** Run as Administrator
- **Linux/macOS:** Use `sudo` when required

---

## 8) Example Workflows

### From Catalog
1. Load or auto-detect `apps.info`
2. Search, double-click to add
3. Add directories
4. Save and install

### Dry Run Mode
Preview commands before running installs.

---

## 9) Credits

Built as part of **“50 Days • 50 Projects”** challenge.  
Author: Sattyam Chavan — MIT License.
