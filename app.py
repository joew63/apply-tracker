from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from database import app_create, add_company, add_application, get_all_companies, get_all_applications, clear_companies, update_application, create_user, get_user_by_email
from dotenv import load_dotenv
from functools import wraps
from email_validator import validate_email, EmailNotValidError
import os, bcrypt

app = Flask(__name__)
load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY environment variable is not set")
app_create()

def login_required(original_function):
    @wraps(original_function)
    def wrapper(*args, **kwargs):
        if "user_id" in session:
            return original_function(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # handle the form submission
        email = request.form.get('email')
        password = request.form.get('password')
        user = get_user_by_email(email)
        if user is None or not bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return render_template('login.html', error="Invalid email or password")
        session['user_id'] = user[0]
        return redirect(url_for('main'))
    return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if email is None or password is None:
            return render_template('signup.html', error="Invalid email or password")
        
        try:
            validate_email(email)
        except EmailNotValidError:
            return render_template('signup.html', error="Invalid email")

        if get_user_by_email(email):
            return render_template('signup.html', error="Email already taken")
        
        if password != confirm_password:
            return render_template('signup.html', error="Password does not match")

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        create_user(email, hashed_password)
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route("/", methods=['GET', 'POST'])
@login_required
def main():
    user_id = session['user_id']

    if request.method == 'POST':
        form_type = request.form['form_type']
        if form_type == 'add_company':
            if request.form.get('name').title() != '':
                add_company(user_id, request.form.get('name'))
        elif form_type == 'add_application':
            if request.form.get('role') != '':
                add_application(
                    user_id,
                    request.form.get('name').capitalize(),
                    request.form.get('role'),
                    request.form.get('status'),
                    request.form.get('date_applied'),
                    request.form.get('notes')
                )
        elif form_type == 'clear_database':
            clear_companies(user_id)
            return redirect(url_for('main', cleared='true'))
        return redirect(url_for('main'))

    companies = get_all_companies(user_id)
    applications = get_all_applications(user_id)
    return render_template('index.html', companies=companies, applications=applications)


@app.route("/update", methods=['POST'])
@login_required
def update():
    user_id = session['user_id']
    data = request.get_json()
    update_application(
        user_id,
        data['id'],
        data['role'],
        data['status'],
        data['date_applied'],
        data['notes']
    )
    return jsonify({'success': True})

@app.route("/logout", methods=['POST'])
def logout():
    session.pop("user_id", None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)