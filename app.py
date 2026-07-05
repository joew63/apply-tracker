from flask import Flask, render_template, request, redirect, url_for
from database import app_create, add_company, add_application, get_all_companies, get_all_applications, clear_companies

app = Flask(__name__)
app_create()

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
                    request.form.get('status').capitalize(),
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

if __name__ == "__main__":
    app.run(debug=True)