# Apply Tracker

A full stack web app to track internship and job applications, built with Flask and SQLite.

> **Note:** This project was built as a learning exercise to explore Flask, relational databases, and frontend development. It is intended for personal use.

## What it does

- Add companies you are applying to
- Log applications with role, status, date applied, and notes
- View all companies and applications in a live dashboard
- Color coded status badges (Applied, Interview, Offer, Rejected)
- Toggle between dark and light mode

## Technologies used

- Python
- Flask
- Jinja2
- SQLite3
- HTML/CSS

## Project structure

- `app.py` — Flask routes and request handling
- `database.py` — all SQLite database operations (create, insert, query)
- `templates/index.html` — frontend template rendered by Flask
- `static/style.css` — styling and dark/light mode theming

## Setup

Clone the repo:
```bash
git clone https://github.com/y6367/apply-tracker.git
cd apply-tracker
```

Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## How to run it

```bash
python3 app.py
```

Then visit `http://127.0.0.1:5000` in your browser.

## Database

Two related tables power the app:

- `companies` — stores unique companies
- `applications` — stores applications, linked to companies via a foreign key

The database file `applications.db` is created automatically on first run and is excluded from version control.
