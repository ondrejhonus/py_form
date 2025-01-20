from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp
from models import db, Person

# Initialize the Flask app and configure the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Path to database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
app.config['SECRET_KEY'] = 'mysecretkey'  # Secret key for CSRF protection

# Initialize the database
db.init_app(app)

# WTForm for adding a new person with validators
class PersonForm(FlaskForm):
    # Adding a custom regex validator to ensure that the name contains no numbers
    name = StringField('Name', validators=[
        DataRequired(), 
        Length(min=2, max=50),
        Regexp(r'^[A-Za-z\s]+$', message="Name cannot contain numbers or special characters.")
    ])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=120)])
    submit = SubmitField('Add Person')

@app.route('/')
def index():
    persons = Person.query.all()
    return render_template('index.html', persons=persons)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = PersonForm()
    
    if form.validate_on_submit():
        new_person = Person(name=form.name.data, age=form.age.data)
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
