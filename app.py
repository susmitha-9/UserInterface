from flask import Flask, render_template, url_for,flash,redirect, request
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import email_validator

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange
from datetime import date

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret string'

Bootstrap(app)

db_name = 'Users.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    number = db.Column(db.Integer)
    location = db.Column(db.String)
    password = db.Column(db.String)
    confirm_password = db.Column(db.String)

    def __init__(self, username, email, number, location, password, confirm_password):
        self.username = username
        self.email = email
        self.number = number
        self.location = location
        self.password = password
        self.confirm_password = confirm_password

class AddRecord(FlaskForm):
  
    id_field = HiddenField()
    username = StringField('Username', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid username"),
        Length(min=3, max=25, message="Invalid username length")
        ])
    email = StringField('Email', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\'\/]+$', message="Invalid email"),
        Length(min=3, max=25, message="Invalid email length")
        ])
    number = IntegerField('Number', [ InputRequired(),
        NumberRange(min=1, max=999, message="Invalid range")
        ])
    location = StringField('Location', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid location"),
        Length(min=3, max=25, message="Invalid location length")
        ])
    password = StringField('Password', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\'\/]+$', message="Invalid password"),
        Length(min=3, max=25, message="Invalid password length")
        ])    
    confirm_password = StringField('Confirm Password', [ InputRequired(),
        Regexp(r'^[A-Za-z\s\-\'\/]+$', message="Invalid password"),
        Length(min=3, max=25, message="Invalid password length")
        ])
    submit = SubmitField('Add Record')        

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/events')
def events():
    return render_template('events.html')



@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form['username']
        email = request.form['email']
        number = request.form['number']
        location = request.form['location']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        record = User(username, email, number, location, password, confirm_password)
        db.session.add(record)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form, field).label.text,
                    error
                ), 'error')        
                return render_template('register.html',title='Register',form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            flash('You have been logged in!',
             'success')
            return redirect(url_for('home'))
    else:
        return render_template('login.html', title='Login', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', pagetitle="404 Error - Page Not Found", pageheading="Page not found (Error 404)", error=e), 404

@app.errorhandler(405)
def form_not_posted(e):
    return render_template('error.html', pagetitle="405 Error - Form Not Submitted", pageheading="The form was not submitted (Error 405)", error=e), 405

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', pagetitle="500 Error - Internal Server Error", pageheading="Internal server error (500)", error=e), 500

if __name__ == '__main__':
    app.run(debug=True)
