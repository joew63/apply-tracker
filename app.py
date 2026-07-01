from flask import Flask, render_template, request, redirect, url_for
from database import app_create, add_company, add_application

app = Flask(__name__)
app_create()

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        form_type = request.form['form_type']
        if form_type == 'add_company':
            add_company(request.form.get('name'))
        elif form_type == 'add_application':
            add_application(
                request.form.get('name'),
                request.form.get('role'),
                request.form.get('status'),
                request.form.get('date_applied'),
                request.form.get('notes')
            )
        return redirect(url_for('main'))
    print('hello')
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)