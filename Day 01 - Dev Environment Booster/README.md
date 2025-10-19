# 🚀 Dev Environment Booster (GUI)

> **Day 01** of the *“50 Days • 50 Projects”* Challenge  
> Build a one-click setup tool to install your essential development apps and create workspace folders with a clean graphical interface.

---

## 🧩 Overview

The **Dev Environment Booster** is a Python-based GUI utility that automates the process of setting up a fresh development workstation.  
It allows you to:

- 🧱 **Install multiple apps** automatically using your system’s package manager  
- 🗂️ **Create predefined directories** (e.g., `C:/Projects`, `C:/DevTools`)  
- 🧭 **Manage configs visually** — open, edit, and save `setup.JSON`  
- 🔍 **Search from a built-in app catalog (`apps.info`)** and add entries with one click  
- 🧪 **Dry-run mode** to preview actions before real installation  
- 📜 **Live logs** for every operation  

---

## 📁 Project Structure

```
📦 Dev Environment Booster
 ┣ 📂 docs/
 ┃ ┣ 📄 README.md
 ┃ ┗ 📄 USAGE.md
 ┣ 📂 src/
 ┃ ┣ 📄 gui_setup_booster.py
 ┃ ┣ 📄 setup.JSON
 ┃ ┗ 📄 apps.info
 ┣ 📄 HowToRun.txt
 ┗ 📄 LICENSE
```

---

## 🧠 Key Features

| Feature | Description |
|----------|-------------|
| **GUI Config Manager** | Add/remove apps and paths visually |
| **Smart Detection** | Detects package managers automatically |
| **Pre-Check Installs** | Detects already installed packages |
| **Catalog Search** | Browse 100+ developer tools from `apps.info` |
| **Dry-Run Mode** | Preview all commands before running |
| **Threaded Execution** | Keeps GUI responsive during installs |
| **Real-Time Logging** | Logs everything in a live console |

---

## ⚙️ Supported Platforms

| OS | Package Manager |
|----|------------------|
| 🪟 Windows | `winget` |
| 🐧 Linux | `apt`, `dnf`, `pacman` |
| 🍎 macOS | `brew` |

---

## ▶️ How to Run

```bash
cd src
python gui_setup_booster.py
```

> Run as Administrator on Windows or with `sudo` on Linux/macOS.

---

## 🗂️ Configuration Files

### setup.JSON
```
Your editable working configuration.

```

## apps.info

```

A catalog of popular developer apps for quick selection.

---

## 🧱 Built With

| Library | Purpose |
|----------|----------|
| `tkinter`, `ttk` | GUI design |
| `subprocess` | Execute installation commands |
| `threading`, `queue` | Run tasks in background threads |
| `json` | Handle setup and catalog data |
| `os`, `platform`, `shutil` | Manage paths and detect OS |

---

## 🧾 License

Licensed under the **MIT License** — see `LICENSE` file for details.

---

## 👨‍💻 Author

**Sattyam Chavan**  

