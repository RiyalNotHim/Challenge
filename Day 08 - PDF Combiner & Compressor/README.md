I cannot generate or attach .zip files, but I can provide all the individual files and code you need to create the complete PDF Combiner & Compressor project.

This project uses a tabbed interface (Merge & Compress) and requires an external library, PyMuPDF, which is the standard for PDF manipulation in Python.

📂 Directory Structure
PDF_Utility/
├── docs/
│   ├── HowToRun.txt
│   └── USAGE.md
├── src/
│   └── app.py
├── LICENSE
├── README.md
└── requirements.txt
📄 README.md
(This is the main file for the project root.)

Markdown

# 📄 PDF Combiner & Compressor
> **A GUI Utility to Merge, Compress, and Automate PDF Workflows**

The **PDF Combiner & Compressor** is a desktop tool built with Python and Tkinter to handle common PDF tasks efficiently.  
It provides a simple, two-tab interface to merge multiple documents into one, or compress large files for easy sharing.

---

## 🚀 Overview

This application is designed to be a simple, fast, and lightweight solution for document management. It runs entirely on your local machine, ensuring file privacy.

With this tool, you can:
-   **Merge PDFs:** Add multiple PDF files, re-order them, and combine them into a single, new document.
-   **Compress PDFs:** Add one or more files and apply effective compression to reduce their file size.
-   **Batch Processing:** The compression tab fully supports batch operations—add dozens of files and compress them all with one click.
-   **Live Logs:** See a real-time log of all operations.

---

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 🧱 **Tabbed Interface** | A clean GUI with separate tabs for "Merge" and "Compress" workflows. |
| 🔄 **Drag & Drop Ordering** | Easily re-order files in the merge list using "Move Up" / "Move Down" buttons. |
| ⚙️ **Batch Compression** | Add multiple files to the compress queue and process them all at once. |
| ⚡ **Efficient Backend** | Uses the powerful **PyMuPDF (fitz)** library for high-speed merging and effective compression. |
| 📜 **Live Log Panel** | A log panel shows the status of each operation, including success or error messages. |
| 🪟 **Modern GUI** | Built with Tkinter and `ttk` using a clean, dark-mode theme. |

---

## 🧠 Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Frontend (GUI)** | Tkinter, ttk (Python Standard Library) |
| **Core PDF Logic** | PyMuPDF (fitz) |
| **Core Logic** | Python 3 (Threading, OS) |

---

## 🗂️ Folder Structure

PDF Combiner and Compressor/
├── docs/
│   ├── HowToRun.txt
│   └── USAGE.md
├── src/
│   └── app.py
├── LICENSE
├── README.md
└── requirements.txt

---

## ⚡ Installation & Usage

### 1. Create the Files
Create the directory and files as shown in the structure above.

### 2. Install Dependencies (Important)
> 💡 This project requires an external library, `PyMuPDF`.

```bash
# Navigate to the root of the project
cd PDF_Utility/

# Install the required library
pip install -r requirements.txt
3. Run the Application
Bash

# Run the app
python src/app.py
4. Use the App
Click the "Merge PDFs" tab to combine files.

Click the "Compress PDFs" tab to reduce file sizes.

📘 Documentation
For detailed workflow instructions:

See docs/USAGE.md