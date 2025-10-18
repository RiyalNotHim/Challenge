# Usage

## 1) Edit Configuration
Update `src/config.example.json` with the packages, pip/npm modules, and VS Code extensions you want.

## 2) Run on Windows (PowerShell)
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\src\setup.ps1 -ConfigPath .\src\config.example.json -DryRun:$false
```

Dry run:
```powershell
.\src\setup.ps1 -ConfigPath .\src\config.example.json -DryRun
```

## 3) Run on macOS/Linux (Bash)
```bash
chmod +x ./src/setup.sh
./src/setup.sh --config ./src/config.example.json
```

Dry run:
```bash
./src/setup.sh --config ./src/config.example.json --dry-run
```
