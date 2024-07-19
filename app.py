from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError

app = Flask(__name__)

app.config['SECRET_KEY'] = "kia"

# Form Class
class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[('1', 'Volunteer'), ('2', 'Administrator')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


# add more in DB when pulling data from there
states = [
    {'code': 'AL', 'name': 'Alabama'},
    {'code': 'AK', 'name': 'Alaska'},
    {'code': 'AZ', 'name': 'Arizona'},
    {'code': 'AR', 'name': 'Arkansas'},
    {'code': 'CA', 'name': 'California'},
    {'code': 'CO', 'name': 'Colorado'},
]
#sample until DB
skills = [
    'Planning and scheduling', 'Problem-solving', 'IT support', 'Photography', 'Workshop facilitation'
]

users = {}
profiles = {}

@app.route("/")
def index():
    form = LoginForm()
    return render_template("index.html", form = form)

@app.route("/login", methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = users.get(email)
        
        if user and user['password'] == password:
            session['email'] = email
            flash(f"Welcome back, {profiles[email]['full_name']}!", "success")
            return redirect(url_for('profile',email=email))
        else:
            flash("Invalid email or password.", "danger")
    
    return render_template("index.html", form=form)


@app.route("/about") # flask url_for 
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit(): #validating
        email = form.email.data
        password = form.password.data
        role = form.role.data
        
        users[email] = {'password': password, 'role': role} # storing
        return redirect(url_for('profile',email=email))

    return render_template("register.html", form=form)

@app.route("/profile/<email>", methods=['GET', 'POST'])
def profile(email):
    # captures data entered from profile.html
    if request.method == 'POST':

        full_name = request.form['full_name']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        skills_selected = request.form.getlist('skills')
        preferences = request.form['preferences']
        availability_dates = request.form.getlist('availability[]')

        # save to database add later
        profiles[email] = {
            'full_name': full_name,
            'address1': address1,
            'address2': address2,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'skills': skills_selected,
            'preferences': preferences,
            'availability': availability_dates
        }

        return redirect(url_for('index')) # place holder
    return render_template("profile.html", states=states, skills=skills, email=email)

@app.route("/notificationSystem")
def notificationManager():
    return render_template("notificationSystem.html");


@app.route("/notification", methods=['GET','POST'])
def notification():
    if request.method == 'POST':

        notifName = request.form['notifName']
        notifDesc = request.form['notifDesc']

        return "Notification Created"
    return render_template("notification.html");

@app.route("/eventManager", methods=['GET','POST'])
def eventManager():
    if request.method == 'POST':

        eventName = request.form['eventName']
        eventDesc = request.form['eventDesc']
        eventDate = request.form['eventDate']
        urgency = request.form['urgency']
        eventAddress = request.form['eventAddress']
        country = request.form['country']
        state = request.form['state']
        zipcode = request.form['zipcode']
        requiredSkills = request.form['requiredSkills']

        return "Event created/updated"
    return render_template("eventManager.html");

@app.route("/event")
def event():
    return render_template("event.html")

@app.route("/volunteer")
def volunteer():
    return render_template("volunteerMatching.html")

@app.route("/admin")
def admin():
    return render_template("adminMatching.html")

@app.route("/history")
def history():
    return render_template("history.html")

if __name__ == '__main__': app.run(host='0.0.0.0', debug=True) # starts server