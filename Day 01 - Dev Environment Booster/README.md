# ⚙️ Dev Environment Booster  
> **A Smart One-Click Developer Machine Setup Tool Built with Python**

The **Dev Environment Booster** is an open-source automation utility that simplifies setting up a development workstation.  
It combines intelligent package installation and directory management into a clean, **Tkinter-powered GUI** — so you can install your essential tools and organize your workspace in minutes.

---

## 🚀 Overview

Configuring a new system for development often requires repetitive manual work — installing tools, SDKs, editors, and setting up project directories.  
This app provides a **single graphical interface** to automate that process.  

With just one click, you can:
- Install **multiple developer tools** through your system’s package manager.
- Automatically create common **workspace directories**.
- Save and reuse setup configurations across different machines.
- Load a full app catalog (`apps.info`) and select tools visually.
- View **real-time logs** of every operation inside the GUI.

---

## ✨ Features

| Feature | Description |
|----------|-------------|
| 🧱 **One-Click Setup** | Install all your developer tools automatically using `winget`, `apt`, `dnf`, or `brew`. |
| 🔍 **App Catalog** | Built-in searchable catalog (`apps.info`) of 100+ essential developer tools. |
| ⚙️ **Config Manager** | Add, remove, and save app lists and workspace paths in `setup.JSON`. |
| 🧪 **Dry Run Mode** | Preview installation commands before applying changes. |
| 📂 **Directory Creator** | Automatically creates folders like `C:/Projects`, `C:/DevTools`, etc. |
| 📜 **Live Logs** | Displays all actions in real time for better visibility and debugging. |
| 🧭 **Smart Detection** | Detects available package manager automatically for your OS. |
| 🪟 **Simple GUI** | Clean Tkinter-based interface with responsive layouts. |

---

## 🧠 Tech Stack

| Component | Technology Used |
|------------|----------------|
| **Frontend (GUI)** | Tkinter (Python Standard Library) |
| **Backend / Core Logic** | Python 3.10+ |
| **Package Management** | winget / apt / dnf / brew |
| **Platform Support** | Windows, Linux, macOS |

---

## 🗂️ Folder Structure

```
dev_environment_booster/
├── docs/
│   ├── USAGE.md
│   ├── screenshots/
│   │   └── gui_main.png
│
├── src/
│   ├── gui_setup_booster.py
│   ├── setup.JSON
│   └── apps.info
│
├── README.md
├── HowToRun.txt
└── LICENSE
```

---

## ⚡ Installation & Usage

### 1️⃣ Clone or Download
```bash
git clone https://github.com/yourusername/dev-environment-booster.git
cd dev-environment-booster/src
```

### 2️⃣ Run the Application
> 💡 *Run as Administrator (Windows) or with sudo (Linux/macOS) for full installation access.*

```bash
python gui_setup_booster.py
```

### 3️⃣ Configure Your Setup
- Load or create a new `setup.JSON`
- Add apps manually or from the **Catalog Panel**
- Add desired workspace directories
- Enable **Dry Run** if you just want to preview
- Click **Install Apps** and **Create Directories**

---

## 📘 Documentation

For detailed setup, configuration, and workflow:
- See [`docs/USAGE.md`](docs/USAGE.md)
- Learn about JSON file formats and error handling

---

## 🧩 Why JSON + GUI?

- Easy to export and share your environment setup.  
- Reusable across multiple devices and teams.  
- JSON makes automation flexible; GUI makes it accessible.

---

## 🧱 Future Enhancements

- 🧰 Add **“Auto Resolve”** for ambiguous package names.  
- 💾 Add **Import/Export Profile** feature for teams.  
- 🌈 Introduce a **Dark Mode** for the interface.  
- 📦 Package into standalone **EXE** via PyInstaller.  
- ☁️ Cloud sync for developer environment presets.

---

## 📄 License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

## 👨‍💻 Author

**Sattyam Chavan**  
📧 *Feel free to fork, enhance, or contribute!*   
⭐ If you like this project, don’t forget to star the repo on GitHub!

---

> “Automate the boring setup — so you can start building faster.” ⚡
