from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
import random
import string
import os
from database import get_db_connection

# App configuration
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your_very_secret_key_change_this'
DB_FILE = os.path.join(os.path.dirname(__file__), 'urls.db')

def get_db():
    """Opens a new database connection if one is not already open."""
    if 'db' not in g:
        g.db = get_db_connection()
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """Closes the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def generate_short_code(length=6):
    """Generates a random alphanumeric short code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET'])
def index():
    """Main dashboard page. Shows form and all links."""
    db = get_db()
    links = db.execute('SELECT * FROM links ORDER BY id DESC').fetchall()
    base_url = request.host_url
    return render_template('index.html', links=links, base_url=base_url)

@app.route('/shorten', methods=['POST'])
def shorten():
    """Endpoint to create a new short link."""
    original_url = request.form['original_url']
    custom_code = request.form['custom_code'].strip()
    
    if not original_url:
        flash('Original URL is required!', 'error')
        return redirect(url_for('index'))

    db = get_db()
    
    if custom_code:
        # User provided a custom code
        existing = db.execute('SELECT * FROM links WHERE short_code = ?', (custom_code,)).fetchone()
        if existing:
            flash(f"Custom code '{custom_code}' is already taken!", 'error')
            return redirect(url_for('index'))
        short_code = custom_code
    else:
        # Generate a new short code
        while True:
            short_code = generate_short_code()
            existing = db.execute('SELECT * FROM links WHERE short_code = ?', (short_code,)).fetchone()
            if not existing:
                break
    
    try:
        db.execute(
            'INSERT INTO links (original_url, short_code) VALUES (?, ?)',
            (original_url, short_code)
        )
        db.commit()
        flash(f"Success! Your short link is ready.", 'success')
    except sqlite3.Error as e:
        flash(f"An error occurred: {e}", 'error')

    return redirect(url_for('index'))

@app.route('/<string:short_code>')
def redirect_to_url(short_code):
    """Redirect endpoint. Finds link, logs click, and redirects."""
    db = get_db()
    link = db.execute('SELECT * FROM links WHERE short_code = ?', (short_code,)).fetchone()
    
    if link:
        # Increment click count
        try:
            db.execute(
                'UPDATE links SET clicks = clicks + 1 WHERE short_code = ?',
                (short_code,)
            )
            db.commit()
        except sqlite3.Error as e:
            print(f"Error incrementing click: {e}")
            
        # Redirect to the original URL
        return redirect(link['original_url'])
    else:
        # If the link doesn't exist, go to the home page
        flash(f"Short link '{short_code}' not found.", 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Check if DB exists before running
    if not os.path.exists(DB_FILE):
        print("Database not found!")
        print("Please run 'python src/database.py' to initialize the database.")
    else:
        print("Starting Flask server at http://127.0.0.1:5000")
        app.run(debug=True)