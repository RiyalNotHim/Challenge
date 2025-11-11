# 🧹 File Organizer Bot — Usage & Technical Guide

> **Purpose:** A simple GUI tool to sort files in a directory based on their extension or modification date.

---

## 1) What This App Does

This tool provides a GUI to clean a "target" directory (like "Downloads"). It moves files from the main directory into subfolders based on your chosen sort strategy.

-   **GUI:** Allows you to pick a folder, choose a sort mode, and start the process.
-   **Logging:** A text box shows a live log of every file that is moved.
-   **Non-Blocking:** The sorting runs in a separate thread so the GUI doesn't freeze.
-   **Safe:** It only moves files, it will skip any sub-directories it finds.

---

## 2) Sort Modes Explained

### Mode 1: Sort by Extension

This is the default mode. It reads the `data/config.json` file to build a map of file types.

1.  It scans every file in the target directory.
2.  It checks the file's extension (e.g., `.pdf`).
3.  It looks up that extension in its map (e.g., `.pdf` maps to "Documents").
4.  It creates the "Documents" folder if it doesn't exist.
5.  It moves the file into `TargetDirectory/Documents/`.

> **Uncategorized Files:** Any file whose extension is **not** in `config.json` will be moved to a folder named **"Other"**.

### Mode 2: Sort by Date (YYYY-MM-DD)

This mode ignores file types and uses the **file modification date**.

1.  It scans every file.
2.  It checks the file's "last modified" timestamp.
3.  It formats this date as `YYYY-MM-DD` (e.g., `2025-11-12`).
4.  It creates a folder with that name if it doesn't exist.
5.  It moves the file into `TargetDirectory/2025-11-12/`.

### Mode 3: Sort by Date (YYYY-MM)

This is the same as above, but groups files by month.

1.  It gets the modification date.
2.  It formats it as `YYYY-MM` (e.g., `2025-11`).
3.  It moves the file into `TargetDirectory/2025-11/`.

---

## 3) Customizing the Configuration

You can easily change the "Sort by Extension" behavior by editing `data/config.json`.

**To add a new file type:**
Find the right category (e.g., "Images") and add the new extension (e.g., `".tiff"`) to the list.

**To add a new category:**
Add a new key-value pair to the `extension_mappings` object. For example, to add a "Fonts" category:

```json
{
  "extension_mappings": {
    "Images": [".jpg", ".png"],
    "Documents": [".pdf"],
    "Fonts": [".ttf", ".otf", ".woff"],
    "...": "..."
  }
}