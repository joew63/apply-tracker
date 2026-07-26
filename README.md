# Apply Tracker

A full stack web app to track internship and job applications, built with Flask and SQLite — with session-based authentication protecting the dashboard.

> **Note:** This project was built as a learning exercise to explore Flask, relational databases, authentication, and frontend development. It is intended for personal use.

## What it does

- Sign up and log in with an email and password — passwords are hashed with bcrypt, never stored in plain text
- All dashboard routes are protected — visiting the app while logged out redirects to the login page
- Add companies you are applying to
- Log applications with role, status, date applied, and notes
- View all companies and applications in a live dashboard
- Inline edit applications — update role, status, date, and notes without leaving the page
- Archive applications to visually strike them out
- Color coded status badges (Applied, Interview, Offer, Rejected)
- Delete individual applications
- Clear all data with a double confirm button — autoincrement resets to 1 on clear
- Toggle between dark and light mode
- Log out from the dashboard header

## Technologies used

- Python
- Flask (with Flask's built-in client-side sessions for auth)
- bcrypt (password hashing)
- email-validator (signup email format validation)
- python-dotenv (loading the app's secret key from environment variables)
- Jinja2
- SQLite3
- HTML/CSS
- JavaScript

## Project structure

- `app.py` — Flask routes, request handling, and authentication (signup, login, logout, route protection)
- `database.py` — all SQLite database operations (create, insert, query, update, delete, clear), including user account storage
- `templates/index.html` — main dashboard, rendered by Flask
- `templates/login.html` — login page
- `templates/signup.html` — account creation page
- `static/style.css` — styling and dark/light mode theming for the dashboard
- `static/auth.css` — styling for the login/signup pages
- `static/main.js` — all client side JavaScript (theme toggle, inline editing, archive, clear confirm)

## Setup

Clone the repo:
```bash
git clone https://github.com/joew63/apply-tracker.git
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

Create a `.env` file in the project root with a secret key, used to sign login sessions:
```
SECRET_KEY=your-randomly-generated-secret-key-here
```
Generate one with:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```
`.env` is excluded from version control — never commit your real secret key.

## How to run it

```bash
python3 app.py
```

Then visit `http://127.0.0.1:5000` in your browser. You'll be redirected to the login page — use the "Sign up" link to create an account first.

## Database

Three tables power the app:

- `users` — stores registered accounts (email, bcrypt password hash)
- `companies` — stores unique companies
- `applications` — stores applications linked to companies via a foreign key

The `company_id` foreign key relationship ensures every application references a valid company. Clearing the database also resets SQLite's internal `sqlite_sequence` table, so autoincrement ids restart from 1.

The database file `applications.db` is created automatically on first run and is excluded from version control.

## Security notes

- Passwords are hashed with bcrypt before storage — the app never stores or logs a plain-text password.
- Sessions are Flask's built-in client-side sessions: session data is signed (not encrypted) and stored in a cookie, verified against `SECRET_KEY` on every request.
- Login and signup return the same generic error message ("Invalid email or password") on failure, so a failed attempt doesn't reveal whether a given email has an account.
- Logout is a `POST`-only route, so it can't be triggered by a plain link or embedded image.

## Roadmap

- Scope companies/applications per logged-in user (currently, all logged-in users share the same dashboard data — this is the next planned step)
- Filter applications by status
- Add application success rate stats
- Persist archived state to the database