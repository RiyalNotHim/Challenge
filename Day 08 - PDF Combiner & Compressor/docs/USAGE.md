# 📄 PDF Utility — Usage & Technical Guide

> **Purpose:** A tabbed GUI tool to merge and compress PDF files,
> with support for batch operations.

---

## 1) What This App Does

This tool provides a two-part GUI to manage PDF files. It uses the `PyMuPDF` (fitz) library, which is fast and efficient.

-   **Tab 1: Merge PDFs:** Lets you combine multiple PDF files into one.
-   **Tab 2: Compress PDFs:** Lets you process one or more files to reduce their file size.
-   **Log Panel:** A log at the bottom shows the status of all actions.

---

## 2) Workflow: Merge PDFs

This tab is for combining several documents into a single file.

1.  Click **"Add PDF(s)"** and select all the files you want to merge. They will appear in the list.
2.  **Order is important.** The files will be merged from top to bottom.
3.  Select a file in the list and use the **"Move Up"** and **"Move Down"** buttons to set the correct order.
4.  Use **"Remove Selected"** or **"Clear List"** to fix any mistakes.
5.  Once you are happy with the order, click **"Merge and Save As..."**
6.  A "Save" dialog will appear. Choose a name and location for your new merged PDF.
7.  The log will show "Merge complete!" when done.

---

## 3) Workflow: Compress PDFs (Batch)

This tab is for reducing the file size of one or more documents.

1.  Click **"Add PDF(s)"** and select all the files you want to compress. You can add one file or hundreds.
2.  Use **"Remove Selected"** or **"Clear List"** to manage the queue.
3.  Click **"Compress Selected Files"**.
4.  The app will process **every file** in the list.
5.  It saves a new file with the suffix `_compressed.pdf` **in the same directory** as the original.
    -   `MyFile.pdf` will be saved as `MyFile_compressed.pdf`
6.  The log will update as each file is processed.

> **Note on Compression:** This uses `deflate` and `garbage collection` to optimize the file. It is "lossy" but very effective, especially on PDFs with large, unoptimized images.