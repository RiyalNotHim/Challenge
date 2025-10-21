# GitHub Repo Manager — USAGE

## Purpose
Bulk-manage multiple GitHub repositories (clone/pull/sync) using a single JSON file as the source of truth. Useful for developers, CI admins, and maintainers handling lots of repos.

## JSON Schema (see schema_example.json)
Each entry must contain:
- `name` (optional): friendly name
- `url` (required): git clone URL (HTTPS or SSH)
- `path` (required): local directory path where repo should live (can be relative)
- `branch` (optional): branch to checkout/pull (default: repository's default)
- `auto_push` (optional): boolean — if true, the tool will attempt to push local commits after pulling (use with caution)
- `skip` (optional): boolean — skip this repo

Example entry:
```json
{
  "name": "Swasta-Setu",
  "url": "https://github.com/RiyalNotHim/Swasta-Setu.git",
  "path": "C:\\Programz\\Challenge\\Day 03 - Git Repo Manage\\copys",
  "branch": "main",
  "auto_push": false
}
```

## Basic commands
Run the manager with a JSON list:
```bash
python repo_manager.py repos.json
```
Options:
- `--threads N` parallelize work (default 4)
- `--dry-run` show actions without executing git commands
- `--token <TOKEN>` supply GitHub token for private repos (will use HTTPS auth)
- `--gui` open a simple Tkinter GUI to run tasks interactively

## Notes & safety
- The tool uses local `git` binary via subprocess. Ensure Git is installed and available in PATH.
- `auto_push` will attempt to run `git add/commit/push` only if there are staged/unstaged changes. It will not auto-commit without creating a default message.
- For private repos prefer SSH keys or pass a token. Tokens are used in HTTPS clone URLs and are not stored by the tool.
