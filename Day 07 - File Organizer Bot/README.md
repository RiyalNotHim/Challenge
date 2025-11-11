# 🧹 File Organizer Bot
> **A Smart GUI Utility to Automatically Sort Files by Extension or Date**

The **File Organizer Bot** is a lightweight Python tool that cleans up messy folders (like "Downloads") with a single click.  
It uses a clean **Tkinter-powered GUI** to sort your files into categorized subfolders based on customizable rules.

---

## 🚀 Overview

This application provides a simple graphical interface to select a "target" directory and an organization strategy. It reads a configuration file to know how you want your files sorted.

With this tool, you can:
-   **Sort by Extension:** Move all `.jpg` and `.png` files into an "Images" folder, `.pdf` and `.docx` into "Documents," etc.
-   **Sort by Date:** Group all files into folders named after their modification date (e.g., `2025-11-12` or `2025-11`).
-   **Customize Mappings:** Easily edit the `data/config.json` file to define your own categories and file types.
-   **See Live Logs:** A log panel in the GUI shows exactly which files were moved and where.

---

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 🧱 **Two Sort Modes** | Organize your files by **File Extension** or **Modification Date** (YYYY-MM or YYYY-MM-DD). |
| ⚙️ **JSON Configuration** | All extension-to-folder mappings are stored in an easy-to-edit `data/config.json` file. |
| 📂 **Smart Sorting** | Automatically creates required subfolders (e.g., "Images", "Documents") if they don't exist. |
| 📜 **Live Log Panel** | See a real-time log of all file operations as they happen. |
| 🛡️ **Safe Operation** | Skips directories and system files, only moving files. |
| 🪟 **Simple GUI** | Clean, dark-mode Tkinter interface. Built with only Python's standard library. |

---

## 🧠 Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Frontend (GUI)** | Tkinter (Python Standard Library) |
| **Core Logic** | Python 3 (OS, shutil, datetime) |
| **Configuration** | JSON |

---

## 🗂️ Folder Structure

File Organizer Bot/ 
├── data/ 
│ └── config.json 
├── docs/ 
│ ├── HowToRun.txt 
│ └── USAGE.md 
├── src/ 
│ └── app.py 
├── LICENSE 
└── README.md


---

## ⚡ Installation & Usage

### 1. Create the Files
Create the directory and files as shown in the structure above.

### 2. Run the Application
> 💡 *No installation needed! Just ensure you have Python 3.*

```bash
# Navigate to the root of the project
cd FileOrganizerBot/

# Run the app
python src/app.py
3. Organize Your Files
Click "Browse" and select the folder you want to clean up (e.g., your "Downloads" folder).

Choose your desired "Sort Mode".

Click "Start Organizing".

Watch the log to see your files get sorted!

📘 Documentation
For detailed configuration and sorting logic:

See docs/USAGE.md