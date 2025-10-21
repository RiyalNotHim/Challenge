# 🕒 Process Tracker (GUI + CLI)
> **Day 04 of the “50 Days • 50 Projects” Challenge**  
> Track tasks, sessions, and time — start/stop timers, mark done/reopen, export to CSV, and review detailed logs.

The **Process Tracker** is a lightweight productivity tool that lets you manage tasks and record time spent on them.  
Use the **GUI** for a single‑window experience (controls, grid, stats, details), or run the **CLI** for quick commands and automation.

---

## 🚀 Overview
- Create tasks with title, description, tags, and estimates (in minutes).
- Start/Stop a timer to record working sessions.
- Mark tasks **Done** or **Reopen** them anytime.
- See **Stats** (Totals, Active, Completed, Currently Running).
- View **Task Details & Sessions** pane for the selected task.
- Export a **timesheet CSV** and keep local JSON history.
- Works offline — all data is stored locally.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| ⏱️ Timers | Start/Stop per‑task timers; log sessions automatically |
| 🧩 Task Management | Add, edit (via reopen + manual log), mark Done/Reopen, Delete |
| 📊 Stats | Live aggregate counts: Total, Active, Completed, Running |
| 🗂️ Tags | Simple comma‑separated tags for filtering (future-ready) |
| 📝 Manual Log | Add minutes manually to any task |
| 📤 Export CSV | One‑click export of timesheet for reporting |
| 🖥️ GUI + CLI | Run a Tkinter GUI or a command‑first CLI |
| 💾 Local Storage | Persisted in `data/tasks.json` with timestamped backups |

---

## 🧠 Tech Stack

| Component | Technology |
|----------|------------|
| **GUI** | Tkinter (Python Standard Library) |
| **CLI** | Python argparse / interactive shell |
| **Storage** | JSON files in `data/` (with rolling backups) |
| **OS** | Windows / macOS / Linux |

---

## 🖼️ Screens
Add screenshots to `docs/screenshots/` and update the paths.

| Description | Screenshot |
|-------------|------------|
| Main Window | ![Process Tracker](docs/screenshots/process_tracker_gui.png) |

> Example reference (your output may look similar):  
> ![Example](docs/screenshots/day4_example.png)

---

## 🗂️ Project Structure
```
process_tracker/
├─ docs/
│  ├─ USAGE.md
│  └─ screenshots/
│     └─ process_tracker_gui.png
├─ src/
│  ├─ process_tracker_gui.py      # GUI entry
│  └─ process_tracker.py          # CLI entry (interactive + flags)
├─ data/                          # created at first run (tasks.json + backups)
├─ HowToRun.txt
├─ README.md
└─ LICENSE
```

---

## ⚡ Quick Start

### GUI
```bash
python src/process_tracker_gui.py
```

### CLI (Interactive)
```bash
python src/process_tracker.py
```

### CLI (Examples)
```bash
python src/process_tracker.py --add "Write README" --desc "Draft documentation" --estimate 45 --tags "docs,writing"
python src/process_tracker.py --start 1
python src/process_tracker.py --stop
python src/process_tracker.py --log 1 30          # add 30 minutes to task #1
python src/process_tracker.py --report today
python src/process_tracker.py --export timesheet.csv
```

> All data is stored in `data/tasks.json`. If missing, it is created automatically.

---

## 📚 Documentation
For a deeper look at commands, JSON schema, CSV export, and GUI controls:  
👉 See **[docs/USAGE.md](docs/USAGE.md)**

---

## 🧱 Roadmap
- Search/filter by tags & status
- Edit task title/description inline
- Weekly/Monthly summary dashboards
- Pomodoro mode (work/break cycles)

---

## 📄 License
MIT — see `LICENSE`.

---

## 👤 Author
**Sattyam Chavan**  
Part of the **50 Days • 50 Projects** series.
