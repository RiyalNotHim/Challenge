# Process Tracker CLI — USAGE

## What it does
A small command-line tool to track tasks, record durations, and mark completion status. Ideal for personal productivity, timeboxing, and lightweight time-tracking.

Data is stored locally in `data/tasks.json`.

## Features
- Add tasks with name, description, tags, and estimated duration.
- Start / Stop timer on a task to record work sessions.
- Manually log time entries for a task.
- Mark tasks as completed or reopen them.
- List tasks, show detailed task view, and show reports (today, week, all-time).
- Export tasks or timesheets to CSV.
- Simple CLI interactive menu + optional command arguments.

## Storage
All data is saved in `data/tasks.json`. Backups are created on each run as `data/tasks_backup_<timestamp>.json`.

## Commands (interactive)
- `add` — create a new task
- `list` — show tasks (all / open / completed)
- `start <task_id>` — start timer for a task
- `stop` — stop current running timer
- `log <task_id> <minutes>` — manually add minutes
- `done <task_id>` — mark as complete
- `view <task_id>` — view task details and sessions
- `report [today|week|all]` — show summary report
- `export <file.csv>` — export timesheet to CSV
- `help` — show help
- `exit` — quit

## Example usage
```bash
python src/process_tracker.py       # interactive menu
python src/process_tracker.py --add "Write report" --estimate 60
python src/process_tracker.py --start 1
python src/process_tracker.py --stop
python src/process_tracker.py --report today
```

## Notes
- The tool is lightweight and stores all data locally. Do not rely on it for legal billing.
- Time entries are recorded in minutes and as start/end timestamps.
