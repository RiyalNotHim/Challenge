# 🤖 Task Automator — Usage & Technical Guide

> **Purpose:** A simple GUI to schedule and automate recurring jobs (e.g., scripts, system tasks) with customizable triggers.

---

## 1) What This App Does

This GUI tool manages a list of scheduled tasks and runs them when their triggers are met. It works by:

- Reading and Writing all task configurations to `data/tasks.json`.
- Providing a **GUI** to:
  - **Add** tasks with one of three trigger types.
  - **Remove** existing tasks from the schedule.
  - **View** all currently scheduled tasks.
  - **Monitor** a live log of scheduler activity.
- Running a **background scheduler thread** that checks tasks every 60 seconds.

---

## 2) Supported Trigger Types

The scheduler supports three simple, customizable triggers:

1.  **Daily**
    * **Trigger:** Runs every day at a specific time.
    * **Params:** `Time (HH:MM)`

2.  **Weekly**
    * **Trigger:** Runs on a specific day of the week at a specific time.
    * **Params:** `Day` (e.g., "Monday"), `Time (HH:MM)`

3.  **Interval**
    * **Trigger:** Runs repeatedly, every N minutes.
    * **Params:** `Interval (mins)` (e.g., "30")

> **Note:** The scheduler thread checks the time every **60 seconds**, so intervals are approximate. An interval of 10 minutes will run at the 10-minute check, not necessarily 10 minutes *exactly* from the last run.

---

## 3) Files & Structure

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

## 4) Dependencies (Python Standard Library Only)

This app uses only **Python’s standard library** (no `pip install` needed):

- `tkinter` — GUI toolkit
- `json` — Read/write `tasks.json`
- `os` — Filesystem paths
- `subprocess` — Run the scheduled commands
- `threading` — Run the scheduler in the background
- `datetime`, `time` — Check task trigger times
- `queue` — Thread-safe logging to the GUI

---

## 5) Example Workflows

### Example 1: Schedule a Daily Backup
1.  **Name:** `Run Daily Backup`
2.  **Command:** `python C:/Scripts/backup.py`
3.  **Trigger:** `Daily`
4.  **Time:** `02:30`
5.  Click **Add Task**. The task will now run every night at 2:30 AM.

### Example 2: Run a Weekly Report
1.  **Name:** `Generate Weekly Report`
2.  **Command:** `powershell -File C:/Scripts/gen_report.ps1`
3.  **Trigger:** `Weekly`
4.  **Day:** `Friday`
5.  **Time:** `17:00`
6.  Click **Add Task**. The task will run every Friday at 5:00 PM.

### Example 3: Check Email Every 15 Minutes
1.  **Name:** `Check Mail`
2.  **Command:** `python C:/Scripts/check_mail.py`
3.  **Trigger:** `Interval`
4.  **Interval (mins):** `15`
5.  Click **Add Task**. The scheduler will trigger this command approximately every 15 minutes.