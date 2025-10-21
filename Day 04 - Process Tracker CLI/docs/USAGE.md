# 📘 Process Tracker — Usage & Developer Guide

> GUI + CLI tool to manage tasks and track time locally with JSON storage and CSV export.

---

## 1) Data Model & Storage
All information is stored at `data/tasks.json`. A timestamped backup is created on each run as `data/tasks_backup_<YYYYMMDD_HHMMSS>.json`.

**Task fields**
- `id` (int) — unique task identifier.
- `title` (str) — task name.
- `description` (str) — free‑form notes.
- `tags` (list[str] or comma string) — e.g., `["writing","research"]`.
- `estimate_min` (int) — estimated minutes to complete.
- `status` (str) — `"Open"` or `"Done"`.
- `sessions` (list) — each session contains `start`, `end`, and `minutes`.
- `total_minutes` (int) — running total across sessions + manual logs.
- `running_since` (timestamp or null) — when a timer is active.

**CSV export columns**
- `id`, `title`, `tags`, `estimate_min`, `total_minutes`, `status`,
  `session_start`, `session_end`, `session_minutes`, `exported_at`

---

## 2) GUI Controls (Single‑Window)

**Controls toolbar**
- **Add Task** — create a new task (title, description, estimate, tags)
- **Start** — start timer for the selected task
- **Stop** — stop current running timer
- **Mark Done** — mark selected task as completed
- **Reopen** — change status back to Open
- **Delete** — remove the selected task
- **Manual Log** — add minutes to the selected task
- **Export CSV** — generate a CSV timesheet

**Grid columns**
- **ID** | **Title** | **Est (min)** | **Time Spent** | **Status** | **Running Since** | **Tags**

**Stats panel**
- **Total** | **Active** | **Completed** | **Currently Running**

**Task Details & Sessions**
- Shows the description, tags, estimate, completion flag, aggregated time and session‑by‑session history for the selected task.

---

## 3) CLI Reference

### Start interactive shell
```bash
python src/process_tracker.py
```
Inside the shell, type `help` to list commands.

### One‑shot flags
```bash
# Add, start, stop, manual log, report, export
python src/process_tracker.py --add "Write report" --desc "intro & methods" --estimate 60 --tags "writing,research"
python src/process_tracker.py --start 1
python src/process_tracker.py --stop
python src/process_tracker.py --log 1 30
python src/process_tracker.py --report today
python src/process_tracker.py --export timesheet.csv
```

**Common interactive commands**
- `add` — create a new task
- `list` — show tasks (all / open / completed)
- `start <id>` — start timer on a task
- `stop` — stop current timer
- `log <id> <minutes>` — add minutes manually
- `done <id>` — mark as completed
- `reopen <id>` — change status to open
- `view <id>` — task details & sessions
- `report [today|week|all]` — quick summary report
- `export <file.csv>` — timesheet export
- `exit` — quit

---

## 4) Reports
- **today** — totals for the current day
- **week** — totals for the current week
- **all** — totals across all time

Reports include: count of tasks worked, total minutes, and per‑task totals.

---

## 5) Error Handling & Tips
- If you close the app while a timer is running, the next start will safely recover and close the previously running session at shutdown time.
- If `data/tasks.json` is corrupted, restore from a backup in `data/`.
- For legal/billing use, validate exported CSV data and keep external backups.
- Tag tasks consistently (e.g., `frontend, design`) to filter/export effectively later.

---

## 6) Dev Notes
- GUI uses Tkinter widgets: `Treeview`, `Text`, `Label`, `Button`, `Toplevel` dialogs.
- Background timer updates are scheduled with `after()` (e.g., 1000ms).
- All filesystem writes are atomic (write to temp → replace).

---

## 7) FAQ
**Q:** Can I edit a task’s title or description?  
**A:** Use **Reopen** then the edit dialog (or update JSON directly between runs).

**Q:** Where is the data kept?  
**A:** `./data/tasks.json` alongside the app. Keep your own backups as well.

**Q:** Can multiple tasks run at once?  
**A:** Only one task should be running at a time; the app enforces a single active timer.

**Q:** Why is my CSV empty?  
**A:** Ensure you have at least one session or manual log on at least one task within the selected export scope.
