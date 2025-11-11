# 🤖 AI Resume Tailor
> **Analyzes job descriptions and resumes to find keyword matches.**

The **AI Resume Tailor** is a desktop utility that helps you quickly optimize your resume for any job application.  
It uses a simple Natural Language Processing (NLP) model to extract and compare the most important keywords from a job description against your resume.

---

## 🚀 Overview

Tailoring a resume for every job is time-consuming. This app streamlines the process by providing a simple, four-panel interface:
1.  **Resume Text:** Paste your full resume.
2.  **Job Description:** Paste the job description.
3.  **Matching Keywords:** Shows you the keywords that are in **both** documents.
4.  **Missing Keywords:** Shows you the top keywords from the job description that are **not** found in your resume.

---

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 🧱 **Keyword Analysis** | Uses `scikit-learn`'s `CountVectorizer` to extract the top 100 1-word and 2-word keywords from the job description. |
| 🔍 **Keyword Matching** | Scans your resume *specifically* for the keywords found in the job description. |
| 🎯 **Targeted Feedback** | Instantly shows you which skills to add to your resume to pass Applicant Tracking Systems (ATS). |
| 📜 **Stopword Filtering** | Ignores common English "stopwords" (e.g., 'and', 'the', 'is') to focus on important nouns and skills. |
| 🪟 **Simple GUI** | Clean, dark-mode Tkinter interface. Built with Python's standard library and `scikit-learn`. |

---

## 🧠 Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Frontend (GUI)** | Tkinter, ttk (Python Standard Library) |
| **Core AI/NLP Logic** | Scikit-learn (`sklearn`) |
| **Core Logic** | Python 3 (Threading) |

---

## _Folder Structure

AI_Resume_Tailor/
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
> 💡 This project requires the `scikit-learn` library.

```bash
# Navigate to the root of the project
cd AI_Resume_Tailor/

# Install the required library
pip install -r requirements.txt
3. Run the Application
Bash

# Run the app
python src/app.py
4. Use the App
Paste your resume text into the top-left panel.

Paste the job description text into the bottom-left panel.

Click "Analyze".

Review the "Matching" and "Missing" keywords in the panels on the right.

📘 Documentation
For detailed workflow instructions:

See docs/USAGE.md