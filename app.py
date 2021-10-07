from flask import Flask, render_template, url_for,flash,redirect
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret string'


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
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))
    else:
     return render_template('register.html',title='Register',form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
    else:
     return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
