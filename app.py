from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

# Initialize the Flask app and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Path to database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
app.config['SECRET_KEY'] = 'mysecretkey'  # Secret key for CSRF protection
db = SQLAlchemy(app)

# Define a class that maps to a database table
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Person {self.name}, {self.age}>"

# Create the tables in the database (only need to run once)
with app.app_context():
    db.create_all()

# WTForm for adding a new person
class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Add Person')

# Routes

@app.route('/')
def index():
    # Get all persons from the database
    persons = Person.query.all()
    return render_template('index.html', persons=persons)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = PersonForm()
    if form.validate_on_submit():
        # Create a new Person object and add it to the database
        new_person = Person(name=form.name.data, age=form.age.data)
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/delete/<int:id>')
def delete(id):
    # Find the person by ID and delete it
    person = Person.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
