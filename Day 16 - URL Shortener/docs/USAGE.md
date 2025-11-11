# 🔗 URL Shortener — Usage & Technical Guide

> **Purpose:** A simple web dashboard to create and track
> short URLs.

---

## 1) How It Works

This application is a simple web server with three main parts:

1.  **Home Page (`/`)**: This is the main dashboard you see. It shows a form to create new links and a table of all existing links and their click counts.
2.  **Shorten Endpoint (`/shorten`)**: When you submit the form, the data is sent here. The app generates a short code, saves the long URL to the database, and then reloads the home page.
3.  **Redirect Endpoint (`/<short_code>`)**: This is the short URL itself. When you click a link like `http://127.0.0.1:5000/myLink`, the app:
    * Finds "myLink" in the database.
    * Adds +1 to its click count.
    * Redirects your browser to the original long URL.

---

## 2) How to Use the App

### To Create a New Link (Random)
1.  Open `http://127.0.0.1:5000` in your browser.
2.  In the "Original URL" box, paste your long link (e.g., `https://www.google.com/maps/place/....`).
3.  Leave the "Custom Short Code" box **empty**.
4.  Click "Shorten".
5.  The page will reload, and your new link (e.g., `/aB3dEf`) will appear in the table.

### To Create a New Link (Custom)
1.  Open `http://127.0.0.1:5000`.
2.  In the "Original URL" box, paste your long link.
3.  In the "Custom Short Code" box, type your desired alias (e.g., `my-project`).
4.  Click "Shorten".
5.  The page will reload, and your custom link (`/my-project`) will appear.
    *Note: You cannot use spaces or special characters. If the code is already taken, it will not work.*

### To Track Clicks
-   Just watch the "Clicks" column in the table on the home page.
-   Every time someone uses a short link, the count for that row will increase when you refresh the page.