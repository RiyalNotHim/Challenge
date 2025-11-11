# 🤖 Task Automator
> **A Simple GUI Job Scheduler for Daily Tasks and Automation Pipelines**

The **Task Automator** is a lightweight utility that simplifies scheduling recurring jobs and scripts.  
It combines a simple trigger system with a clean, **Tkinter-powered GUI** — so you can automate your system maintenance, data pipelines, or daily reminders in seconds.

---

## 🚀 Overview

This application provides a simple graphical interface to manage a list of tasks. It runs a scheduler in the background (while the app is open) to execute your commands at the right time.

With this tool, you can:
- Schedule tasks to run **daily**, **weekly**, or at a repeating **interval**.
- Automatically run any shell command (e.g., `python my_script.py`, `notepad.exe`).
- Add, delete, and manage your task list visually.
- View **real-time logs** of when tasks are executed.
- All tasks are saved persistently in `data/tasks.json`.

---

## ✨ Features

| Feature | Description |
|----------|-------------|
| 🧱 **Custom Triggers** | Schedule tasks to run Daily (at HH:MM), Weekly (on a specific day at HH:MM), or at an Interval (every N minutes). |
| ⚙️ **Simple GUI** | Clean, dark-mode Tkinter interface for managing tasks. |
| 📂 **Persistent Storage** | All scheduled tasks are saved to `data/tasks.json` and reloaded on start. |
| 📜 **Live Logs** | A log panel within the GUI shows which tasks have been triggered. |
| 🐍 **Standard Library** | Runs on **Python 3** with no external dependencies (uses Tkinter, JSON, Threading). |
| 🪟 **Cross-Platform** | Logic is platform-agnostic (Windows, macOS, Linux). |

---

## 🧠 Tech Stack

| Component | Technology Used |
|------------|----------------|
| **Frontend (GUI)** | Tkinter (Python Standard Library) |
| **Backend / Core Logic** | Python 3 (Threading, Subprocess) |
| **Data Storage** | `data/tasks.json` |

---
## 🗂️ Folder Structure

Task Automator/ 
├── data/ 
│ └── tasks.json 
├── docs/ 
│ ├── HowToRun.txt 
│ └── USAGE.md 
├── src/ 
│ └── app.py 
├── LICENSE 
└── README.md

---

## ⚡ Installation & Usage

### 1️⃣ Download or Create Files
Ensure all the files (README, LICENSE, src/app.py, etc.) are created in the structure above.

### 2. Run the Application
> 💡 *No installation needed! Just ensure you have Python 3.*

```bash
# Navigate to the root of the project
cd TaskAutomator/

# Run the app
python src/app.py
3. Schedule Your Tasks
Fill in the task details (Name, Command, Trigger type).

Click "Add Task".

The scheduler is now active as long as the application is running.

📘 Documentation
For detailed setup, configuration, and workflow examples:

See docs/USAGE.md