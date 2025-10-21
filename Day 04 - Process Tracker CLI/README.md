# Process Tracker CLI ⏱️
> Track tasks, durations, and completion status with a lightweight command-line tool.

This repository contains a small CLI utility to help you manage tasks and track time spent on them. Data is stored locally in `data/tasks.json`.

## Features
- Add tasks with title, description, tags, and estimates.
- Start/stop timers to record working sessions.
- Manually log time to tasks.
- Mark tasks as completed.
- List tasks and view detailed sessions.
- Generate reports and export CSV timesheets.
- Interactive shell and non-interactive flags.

## Quick Start
1. Ensure Python 3.8+ is installed.
2. From project root run:
```bash
python src/process_tracker.py
```
This opens the interactive CLI. Use `help` inside for commands.

Non-interactive examples:
```bash
python src/process_tracker.py --add "Write README" --desc "Draft project readme" --estimate 45
python src/process_tracker.py --start 1
python src/process_tracker.py --stop
python src/process_tracker.py --log 1:30
python src/process_tracker.py --report today
python src/process_tracker.py --export timesheet.csv
```

## Files
- `src/process_tracker.py` — main CLI script
- `docs/USAGE.md` — user guide
- `data/tasks.json` — persistent storage (created automatically)
- `HowToRun.txt` — run instructions
- `LICENSE` — MIT license

## Author
Sattyam Chavan
