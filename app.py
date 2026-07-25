from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from database import app_create, add_company, add_application, get_all_companies, get_all_applications, clear_companies, update_application, create_user, get_user_by_email
from dotenv import load_dotenv
from functools import wraps
import json, os, bcrypt

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
            return("nope") # route to login later
    return wrapper


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        form_type = request.form['form_type']
        if form_type == 'add_company':
            if request.form.get('name').title() != '':
                add_company(request.form.get('name').title())
        elif form_type == 'add_application':
            if request.form.get('role') != '':
                add_application(
                    request.form.get('name').capitalize(),
                    request.form.get('role').title(),
                    request.form.get('status'),
                    request.form.get('date_applied'),
                    request.form.get('notes')
                )
        elif form_type == 'clear_database':
            clear_companies()
            return redirect(url_for('main', cleared='true'))
        return redirect(url_for('main'))
    companies = get_all_companies()
    applications = get_all_applications()
    return render_template('index.html', companies=companies, applications=applications)

@app.route("/update", methods=['POST'])
def update():
    data = request.get_json()
    update_application(
        data['id'],
        data['role'].title(),
        data['status'],
        data['date_applied'],
        data['notes']
    )
    return jsonify({'success': True})

if __name__ == "__main__":
    app.run(debug=True)