"""
Personal Portfolio Website - Pudi Venkatesh
Stack: Python Flask + Jinja2 + SQLite (HTML5 / CSS3 frontend only).

Run with:  python app.py
"""

import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database.db"

app = Flask(__name__)
app.secret_key = "portfolio-local-dev-key"  # needed for flash messages

# --------------------------------------------------------------------------
# Portfolio content (passed to the template through Jinja2 variables)
# --------------------------------------------------------------------------

NAME = "Pudi Venkatesh"
TAGLINE = "B.Tech CSE Student | Python Full Stack Intern"
ABOUT = (
    "I am a final-year Computer Science student who enjoys building "
    "web applications with Python, Flask, HTML and CSS."
)
EMAIL = "venkatesh@example.com"

SKILLS = ["Python", "Flask", "HTML5", "CSS3", "JavaScript", "SQL", "Git"]

PROJECTS = [
    {
        "title": "Student Grade Calculator",
        "description": "Console program for marks, grade and result.",
    },
    {
        "title": "Weather Information App",
        "description": "Flask app that shows weather for a city.",
    },
    {
        "title": "Task Management System",
        "description": "Flask and SQLite app with CRUD operations.",
    },
    {
        "title": "Library Management System",
        "description": "Book records with issue and return.",
    },
]


# --------------------------------------------------------------------------
# SQLite helpers
# --------------------------------------------------------------------------

def init_db():
    """Create the database file and contacts table if they do not exist."""
    conn = sqlite3.connect(DATABASE)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def get_contacts():
    """Return all contact rows stored in database.db."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT id, email FROM contacts ORDER BY id").fetchall()
    conn.close()
    return rows


def insert_contact(email):
    """Save one submitted email address into the contacts table."""
    conn = sqlite3.connect(DATABASE)
    conn.execute("INSERT INTO contacts (email) VALUES (?)", (email,))
    conn.commit()
    conn.close()


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    """GET / - render the portfolio page.
    POST / - accept the plain-HTML contact form (no JavaScript needed).
    """
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        if not email:
            flash("Please enter an email address.", "error")
        elif "@" not in email or "." not in email.split("@", 1)[1]:
            flash("Please enter a valid email address.", "error")
        else:
            insert_contact(email)
            flash("Thanks! Your email has been saved.", "success")
        return redirect("/#contact")

    contacts = get_contacts()
    return render_template(
        "index.html",
        name=NAME,
        tagline=TAGLINE,
        about=ABOUT,
        email=EMAIL,
        skills=SKILLS,
        projects=PROJECTS,
        year=datetime.now().year,
        contact_count=len(contacts),
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
