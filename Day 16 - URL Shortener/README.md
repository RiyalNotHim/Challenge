# 🔗 URL Shortener Service
> **A Simple Backend Service with a Web UI to Create and Track Short URLs**

The **URL Shortener** is a lightweight web application that creates short, custom links (like `bit.ly`) and tracks how many times they are clicked.  
It's built with Python, **Flask**, and **SQLite** and provides a simple, clean web interface to manage your links.

---

## 🚀 Overview

This application runs a local web server that captures all requests.
-   When you access the **home page (`/`)**, you get a dashboard.
-   On the dashboard, you can **submit a long URL** to get a short one.
-   You can also **provide a custom alias** (e.g., `/my-link`).
-   When someone accesses your short link (e.g., `http://127.0.0.1:5000/my-link`), the app **logs the click** and **redirects** them to the original long URL.

---

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 🧱 **Link Shortening** | Converts long URLs into 6-character short codes (e.g., `aB3dEf`). |
| ⚙️ **Custom Aliases** | Allows you to define your own short links (e.g., `/resume`). |
| 📈 **Click Tracking** | Counts every time a short link is used. |
| 🪟 **Simple Web UI** | A single-page dashboard to create links and view all stats in a table. |
| ⚡ **Lightweight Stack** | Runs on Flask and SQLite, with no heavy dependencies. |
| 📂 **Persistent Storage** | All links and click counts are saved in a local `urls.db` file. |

---

## 🧠 Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Web Framework** | Flask (Python) |
| **Frontend** | HTML / CSS (via `templates/index.html`) |
| **Database** | SQLite (Python Standard Library) |

---

## 🗂️ Folder Structure

URL Shortener/
├── docs/
│   ├── HowToRun.txt
│   └── USAGE.md
├── src/
│   ├── app.py          # The main Flask web app
│   ├── database.py     # Database setup & functions
│   └── templates/
│       └── index.html  # The web UI
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt

---

## ⚡ Installation & Usage

### 1. Create the Files
Create the directory and files as shown in the structure above.

### 2. Install Dependencies (Important)
> 💡 This project requires the `Flask` library.

```bash
# Navigate to the root of the project
cd URL_Shortener/

# Install the required library
pip install -r requirements.txt
3. Initialize the Database
Before running the app for the first time, you must create the database.

Bash

# Run the database script directly
python src/database.py
This will create an urls.db file inside the src/ folder.

4. Run the Application
Bash

# Run the Flask app
python src/app.py
Your service is now running!

5. Open Your Browser
Open your web browser and go to: http://127.0.0.1:5000

Use the form to create links.

Click the short links in the table to test them.

📘 Documentation
For detailed workflow instructions:

See docs/USAGE.md