# 🧹 Windows Cleanup Assistant  
> **A Simple Yet Powerful Windows Optimization Utility Built with Python**

The **Windows Cleanup Assistant** is an open-source desktop utility designed to free up disk space and optimize your Windows system.  
It uses a clean **Python + PowerShell integration** with a simple **Tkinter-based GUI** for easy system cleanup — no command-line hassle, no external dependencies.

---

## 🚀 Overview

The tool provides quick access to essential cleanup operations that are usually buried deep inside Windows settings.  
With a single click, you can remove **temporary files**, **clear caches**, **flush DNS**, and **empty system logs**, freeing valuable space and improving performance.

---

## ✨ Features

| Feature | Description |
|----------|-------------|
| 🗑️ **Temp File Cleaner** | Deletes temporary files safely from `%TEMP%` directory. |
| 🔁 **Recycle Bin Emptying** | Clears the recycle bin using native PowerShell commands. |
| ⚙️ **Windows Update Cache Cleanup** | Deletes old update files that consume GBs of space. |
| 🖼️ **Thumbnail Cache Cleanup** | Removes old thumbnail caches to refresh media previews. |
| 🌐 **DNS Cache Flush** | Refreshes DNS settings using `ipconfig /flushdns`. |
| 🌍 **Browser Cache Cleaner** | Optionally clears Chrome and Edge cache folders for the current user. |
| 🪟 **GUI Interface** | Built using Tkinter — clean, responsive, and beginner-friendly. |
| 📄 **Live Logs** | Displays output and error logs for every cleanup task in real-time. |

---

## 🧠 Tech Stack

| Component | Technology Used |
|------------|----------------|
| **Frontend (GUI)** | Tkinter (Python Standard Library) |
| **Backend / Core Logic** | Python 3.8+ |
| **System Operations** | Windows PowerShell |
| **Platform Support** | Windows 10 / 11 |

---

## 🖼️ GUI Preview

<p align="center">
  <img src="docs/output.png" alt="Windows Cleanup Assistant GUI" width="700"/>
</p>

---

## 🗂️ Folder Structure

```
windows_cleanup_assistant/
├── docs/
│   ├── USAGE.md
│   ├── output.png
│
├── src/
│   └── win_cleanup_assistant.py
│
├── README.md
├── HowToRun.txt
└── LICENSE
```

---

## ⚡ Installation & Usage

### 1️⃣ Clone or Download
```bash
git clone https://github.com/yourusername/windows-cleanup-assistant.git
cd windows-cleanup-assistant/src
```

### 2️⃣ Run the Assistant
> 💡 *Run as Administrator for maximum effect.*

```bash
python win_cleanup_assistant.py
```

### 3️⃣ Select Cleanup Tasks
Choose the cleanup options from the GUI and click **"Run Cleanup"**.  
Logs will display in real-time inside the app window.

---

## 📘 Documentation

For a complete explanation of:
- what each cleanup task does,  
- safety guidelines,  
- and troubleshooting tips  

👉 Refer to [`docs/USAGE.md`](docs/USAGE.md)

---

## 🧩 Why PowerShell?

PowerShell provides deep access to system functions while ensuring safe and logged execution.  
By integrating PowerShell with Python, we achieve:
- Clear and scriptable control of Windows cleanup tasks.  
- Better safety over direct file deletion via Python.  
- Easier extendibility for system administrators.

---

## 🧱 Future Enhancements

- 🧰 Add **"Dry Run" Mode** for previewing what will be deleted.  
- ⚙️ Integrate **System Restore Point** before cleanup.  
- 💾 Add **Disk Usage Analytics** chart in GUI.  
- 🌈 Create a **Dark Mode** theme for the interface.  
- 📦 Release standalone **EXE build** (PyInstaller).

---

## 📄 License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

## 👨‍💻 Author

**Sattyam Chavan**  
📧 *Feel free to fork, enhance, or contribute!*  
⭐ If you like this project, don’t forget to star the repo on GitHub!

---

> “Small tools make a big difference — keep your system light and clean.” ✨
