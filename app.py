from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from models import db, Person

# Initialize the Flask app and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Path to database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
app.config['SECRET_KEY'] = 'mysecretkey'  # Secret key for CSRF protection

# Initialize the database
db.init_app(app)

# WTForm for adding a new person
class PersonForm(FlaskForm):
    id = IntegerField('ID')
    name = SelectField('Name', choices=[], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Add Person')

# Create the tables and populate initial data if not already present
with app.app_context():
    db.create_all()
    if not Person.query.first():
        db.session.add_all([
            Person(name='Alice', age=30),
            Person(name='Bob', age=25),
            Person(name='Charlie', age=35)
        ])
        db.session.commit()

@app.route('/')
def index():
    persons = Person.query.all()
    return render_template('index.html', persons=persons)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = PersonForm()
    form.name.choices = [(person.name, person.name) for person in Person.query.all()]
    if form.validate_on_submit():
        new_person = Person(name=form.name.data, age=form.age.data, id=form.id.data)
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/delete/<int:id>')
def delete(id):
    person = Person.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
