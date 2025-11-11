# 🤖 AI Resume Tailor — Usage & Technical Guide

> **Purpose:** A GUI tool to extract and compare keywords between a resume
> and a job description.

---

## 1) How It Works (The "AI")

This tool is not magic, but it's smart. It uses a common Natural Language Processing (NLP) technique to find the most important words.

1.  **Text Input:** It takes the raw text from your resume and the job description (JD).
2.  **Stopword Removal:** It filters out common "stopwords" (like 'a', 'the', 'is', 'for', 'with') to focus on meaningful terms.
3.  **Keyword Extraction (from JD):** It scans the job description and builds a vocabulary of the **top 100** most frequent 1-word and 2-word phrases (e.g., "Python", "project management").
4.  **Keyword Scanning (on Resume):** It then takes that *specific* list of 100 keywords and scans your resume to see which ones exist.
5.  **Comparison:**
    * If a top keyword from the JD is found in your resume, it's listed under **"Matching"**.
    * If a top keyword from the JD is **not** found, it's listed under **"Missing"**.

---

## 2) How to Use the App

The interface is split into an "Input" half (left) and an "Output" half (right).

### Input (Left Side)
-   **Top Panel (Resume):** Paste your *entire* resume. Plain text works best.
-   **Bottom Panel (Job Description):** Paste the *entire* job description.

### Output (Right Side)
-   **Analyze Button:** Click this to run the comparison. The app may freeze for a second.
-   **Top Panel (Matching):** This listbox will fill with keywords found in both documents. This is your "green light" list.
-   **Bottom Panel (Missing):** This listbox will fill with keywords from the JD that are *not* in your resume. This is your "to-do" list.

---

## 3) Pro-Tips for Best Results

-   **Focus on the "Missing" List:** This is your action plan. Find ways to naturally include these keywords in your resume (if you have the experience).
-   **Hard Skills:** The tool is best at finding hard skills (e.g., "React", "Java", "SQL", "Agile").
-   **Don't "Keyword-Stuff":** Don't just paste the missing words in white text. The goal is to see that you should rephrase a bullet point, e.g., "Led a team" could become "Led a team using **Agile** methodologies."
-   **Exact Matches:** The tool looks for *exact matches*. "Project Manager" will *not* match "Managed Projects". This mimics how a basic Applicant Tracking System (ATS) works.