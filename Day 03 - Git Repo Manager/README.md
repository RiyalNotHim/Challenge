# 🧩 GitHub Repo Manager  
> **Bulk clone, pull, and sync multiple GitHub repositories — now with an interactive single-window GUI.**

---

## 🚀 Overview
**GitHub Repo Manager** automates the process of handling multiple GitHub repositories with one click.  
Just provide a JSON file containing your repository URLs and local paths — the tool will:
- **Clone** missing repositories  
- **Pull** updates for existing ones  
- Optionally **skip** or **auto-push** selected repos  

The new GUI layout divides the window into three clear sections for easy control and live feedback:
```
+---------------------------------------------------------------+
| Run Tasks (Left)                 | Summary (Right)            |
|---------------------------------------------------------------|
| Logs (Bottom)                                                |
+---------------------------------------------------------------+
```

---

## ✨ Key Features

| Feature | Description |
|----------|-------------|
| 🧭 **Bulk Repo Management** | Clone or update all repositories from one JSON file. |
| ⚡ **Single-Window GUI** | Clean layout: Run Tasks, Summary, and Logs in one interface. |
| 🧱 **Progress Tracking** | Real-time progress bar and completion summary. |
| 🗂️ **Color-Coded Logs** | Success ✅, Fail ❌, Skipped ⚪, and Running 🔵 outputs. |
| 🧰 **Multi-Threaded Backend** | Handles multiple repositories efficiently without freezing the UI. |
| 💾 **Cross-Platform** | Works on Windows, Linux, and macOS. |
| 🧑‍💻 **CLI Support** | Still supports command-line mode for automation. |

---

## 🧠 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Tkinter (Python Standard Library) |
| **Backend** | Python 3.8+ |
| **System Dependency** | Git CLI installed and accessible in PATH |
| **Supported OS** | Windows / Linux / macOS |

---

## 🗂️ Folder Structure

```
github_repo_manager/
├── docs/
│   ├── USAGE.md
│   ├── schema_example.json
│
├── src/
│   └── repo_manager_gui.py      # Updated single-window GUI
│
├── README.md
├── HowToRun.txt
└── LICENSE
```

---

## ⚙️ Installation & Usage

### 1️⃣ Clone or Download
```bash
git clone https://github.com/yourusername/github-repo-manager.git
cd github-repo-manager
```

### 2️⃣ Install Dependencies
Make sure **Python 3.8+** and **Git** are installed on your system.

### 3️⃣ Prepare Your JSON File
Example (`docs/schema_example.json`):
```json
[
  {
    "name": "Swasta-Setu",
    "url": "https://github.com/RiyalNotHim/Swasta-Setu.git",
    "path": "C:\\Programz\\Challenge\\Day 03 - Git Repo Manage\\copys",
    "branch": "main",
    "auto_push": false
  }
]
```

### 4️⃣ Run the GUI
```bash
python src/repo_manager_gui.py
```

---

## 🪟 GUI Layout

### **Run Tasks**
- Select the JSON file of repositories.  
- Click **Run** to start cloning/pulling.  
- Progress bar shows live updates.  

### **Summary**
- Displays total, successful, failed, and skipped repos.  
- Auto-updates as tasks complete.  

### **Logs**
- Shows color-coded real-time feedback.  
- Scrollable text box for large output.  
- "Clear Logs" button for a fresh start.  

---

## 🧩 CLI Mode (Optional)

You can still run this tool in terminal:
```bash
python src/repo_manager.py docs/schema_example.json
```
Options:
- `--dry-run` : Preview actions without executing git commands  
- `--threads N` : Number of parallel threads  
- `--token <TOKEN>` : Use GitHub token for private repos  

---

## 🧱 Future Enhancements
- 🔒 GitHub token manager for private repos  
- 🪄 Auto-push commit with message templates  
- 📊 Visual analytics for repo statistics  
- ☁️ Integration with GitHub API for listing user/org repos  

---

## 📜 License
This project is licensed under the **MIT License**.  
See [`LICENSE`](LICENSE) for more details.

---

## 👨‍💻 Author
**Sattyam Chavan**  
📧 *Feel free to fork, enhance, or contribute!*  
⭐ Don’t forget to star the repo if you find it useful!

---

> “A single click can manage your entire GitHub workspace — make your workflow smarter.” 💡
