from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_data.db'
db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volevel = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    profession = db.Column(db.String(128), nullable=False)
    city_town = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(128), nullable=False)
    volunteer = db.Column(db.Boolean, default=False)
    contact = db.Column(db.String(128), nullable=False)
    remarks = db.Column(db.Text)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    volevel = request.form['volevel']
    name = request.form['name']
    profession = request.form['profession']
    city_town = request.form['city']
    country = request.form['country']
    volunteer = 'vol' in request.form
    contact = request.form['contact']
    remarks = request.form['remarks']

    form_data = FormData(
        volevel=volevel,
        name=name,
        profession=profession,
        city_town=city_town,
        country=country,
        volunteer=volunteer,
        contact=contact,
        remarks=remarks
    )

    db.session.add(form_data)
    db.session.commit()

    return redirect('/')

@app.route('/data_table')
def data_table():
    with app.app_context():
        form_data = FormData.query.with_entities(FormData.name, FormData.profession, FormData.city_town, FormData.country, FormData.remarks).all()
    return render_template('Data_table.html', form_data=form_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)