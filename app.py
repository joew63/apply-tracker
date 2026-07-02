from flask import Flask, render_template, request, redirect, url_for
from database import app_create, add_company, add_application, get_all_applications

app = Flask(__name__)
app_create()

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        form_type = request.form['form_type']
        if form_type == 'add_company':
            add_company(request.form.get('name').capitalize())
        elif form_type == 'add_application':
            add_application(
                request.form.get('name').capitalize(),
                request.form.get('role').title(),
                request.form.get('status').capitalize(),
                request.form.get('date_applied'),
                request.form.get('notes').capitalize()
            )
        return redirect(url_for('main'))
    applications = get_all_applications()
    return render_template('index.html', applications=applications)

if __name__ == "__main__":
    app.run(debug=True)