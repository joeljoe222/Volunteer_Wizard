from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, StringField, PasswordField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.csrf import CSRFProtect
from forms import NotificationForm, EventCreateForm, EventManageForm
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime  # Import the datetime class


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x8f\xda\xe2o\xfa\x97Qa\xfa\xc1e\xab\xb5z\\f\xf3\x0b\xb9\xa5\xb6\xd7.\xc3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


# Define association tables for many-to-many relationships
event_skills = db.Table('event_skills',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)


#database model, still in progress
'''User Profile Management (After registration, users should log in first to complete their profile). Following fields will be on the profile page/form:
Full Name (50 characters, required)
Address 1 (100 characters, required)
Address 2 (100 characters, optional)
City (100 characters, required)
State (Drop Down, selection required) DB will store 2-character state code
Zip code (9 characters, at least 5-character code required)
Skills (multi-select dropdown, required)
Preferences (Text area, optional)
Availability (Date picker, multiple dates allowed, required)
'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    skills = db.relationship('Skill', secondary=user_skills, backref=db.backref('users', lazy='dynamic'))
    #preferencess = db.Column(db.String(200))
    availability = db.Column(db.String(200))

    def __repr__(self):
        return '<Name %r>' % self.id
      
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

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    urgency = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    zipcode = db.Column(db.String(10), nullable=False)
    skills = db.relationship('Skill', secondary=event_skills, backref=db.backref('events', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notifications = db.relationship('Notification', backref='event', lazy=True)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('User', backref='state', lazy=True)
    events = db.relationship('Event', backref='state', lazy=True)



#THIS SITE OUTPUTS CURRENT DATA IN DB: SKILL, EVENT, NOTIFICATION
@app.route("/test")
def test_db_output():
    skills = Skill.query.all()
    states = State.query.all()
    users = User.query.all()
    events = Event.query.all()
    notifications = Notification.query.all()
    return render_template("test.html", skills=skills, states=states, users=users, events=events, notifications=notifications)


#HARDCODED DATA FOR ASSIGNMENT 3
#Example Event
event_data = {
    1 : {
        'event_name':'Example Event One',
        'event_description':'Description for Event One',
        #'event_date':datetime.date(2025, 1, 1),
        'urgency':'1',
        'event_address':'1111 Street Name',
        'event_city':'USA',
        'event_state':'TX',
        'event_zipcode':'11111',
        'required_skills':['a']
    },
    2 : {
        'event_name':'Example Event Two',
        'event_description':'Description for Event Two',
        #'event_date':datetime.date(2025, 2, 2),
        'urgency':'2',
        'event_address':'2222 Street Name',
        'event_city':'USA',
        'event_state':'FL',
        'event_zipcode':'22222',
        'required_skills':['b','c']
    }
}

skill_data = {
    'a':'Skill 1',
    'b':'Skill 2',
    'c':'Skill 3'
}

#Example Notification
notification_data = {
    1:{
        1:{
            'notification_name':'Notification ONE for Event ONE',
            'notification_description':'Notification Description for Event ONE'
        },
        2:{
            'notification_name':'Notification TWO for Event ONE',
            'notification_description':'Notification Description for Event ONE'
        }
        
    },
    2:{
        1:
        {
            'notification_name':'Notification ONE for Event TWO',
            'notification_description':'Notification ONE Description for Event TWO'
        },
        2:
        {
            'notification_name':'Notification TWO for Event TWO',
            'notification_description':'Notification TWO Description for Event TWO'
        },
        3:
        {
            'notification_name':'Notification THREE for Event TWO',
            'notification_description':'Notification THREE Description for Event TWO'
        }
    }
}



# move to db
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

# Sample data
volunteers = [
    {
        'id': 1,
        'name': 'John Doe',
        'skills': 'Communication, Time management, Leadership'
    },
    {
        'id': 2,
        'name': 'John Smith',
        'skills': 'Communication, Time management'
    }
]

events = [
    {
        'id': 1,
        'event_name': 'Early Voting',
        'event_description': 'Early voting for the upcoming elections',
        'location': 'Houston, TX (77490)',
        'event_time': '6:30 PM - 9:30 PM',
        'urgency': 2,
        'required_skills': 'Communication, Time management, Leadership',
        'event_date': '2023-07-15',
        'participation_status': 'Completed',
        'volunteer_id': 1
    },
    {
        'id': 2,
        'event_name': 'Food Drive',
        'event_description': 'Food drive for people in need',
        'location': 'Houston, TX (73031)',
        'event_time': '3:30 PM - 7:30 PM',
        'urgency': 1,
        'required_skills': 'Communication, Time management',
        'event_date': '2023-07-16',
        'participation_status': 'In Progress',
        'volunteer_id': 1
    },
    {
        'id': 3,
        'event_name': 'Community Clean-up',
        'event_description': 'Cleaning up the local community park',
        'location': 'Houston, TX (77002)',
        'event_time': '9:00 AM - 12:00 PM',
        'urgency': 3,
        'required_skills': 'Leadership, Teamwork',
        'event_date': '2023-07-17',
        'participation_status': 'In Progress',
        'volunteer_id': 2
    }
]


# need to remove these by adding it in the DB



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
        user = User.query.filter_by(email=email, password=password).first()
        
        if user:
            session['email'] = email
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for('profile', email=email))
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
        
        new_user = User(
            name='',
            email=form.email.data,
            password=form.password.data,  
            role=form.role.data,
            address='',
            skills='',
            availability=''
        )
        db.session.add(new_user)
        db.session.commit()

        flash("User added, please finish setting up")
        return redirect(url_for('profile',email=form.email.data))

    return render_template("register.html", form=form)

@app.route("/profile/<email>", methods=['GET', 'POST'])
def profile(email):

    # captures data entered from profile.html
    if request.method == 'POST':
        user = User.query.filter_by(email=email).first()
        user.name = request.form['full_name']
        user.address = request.form['address1'] + ' ' + request.form['address2']
        user.skills = request.form['skills']
        user.availability = ', '.join(request.form.getlist('availability[]'))
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('index'))
   
    return render_template("profile.html", states=states, skills=skills, email=email)


#NOTIFICATION SYSTEM -----------------------------------------------------------
@app.route("/notification")
def notification_main():
    notifications = Notification.query.all()
    return render_template("notification-main.html", notifications=notifications)


@app.route("/notification/create", methods=['GET','POST'])
def notification_create():
    form = NotificationForm()
    events = Event.query.all()

    if form.validate_on_submit():
        notification = Notification(
            name = form.name.data,
            description = form.description.data,
            event_id = form.event_id.data
        )
        db.session.add(notification)
        db.session.commit()
        flash(f'Notification Sent! : {form.name.data}','success')
        
        return redirect(url_for('notification_create'))
    return render_template('notification-create.html', form=form)


#EVENT SYSTEM ------------------------------------------------------------------
@app.route("/event")
def event_main():
    events = Event.query.all()
    return render_template("event-main.html", events=events)

@app.route("/event/<int:event_id>")
def event_view(event_id):
    event = Event.query.get_or_404(event_id)
    notifications = Notification.query.filter_by(event_id=event_id).all()
    return render_template("event-view.html", event=event, event_id=event_id, notifications=notifications)

@app.route("/event/create", methods=['GET','POST'])
def event_create():
    form = EventCreateForm()
    form.state.choices = [(state.id, state.name) for state in State.query.all()]
    form.skills.choices = [(skill.id, skill.name) for skill in Skill.query.all()]

    if form.validate_on_submit():
        event = Event(
        name = form.name.data,
        description = form.description.data,
        date = form.date.data,
        urgency = form.urgency.data,
        address = form.address.data,
        city = form.city.data,
        state_id = form.state.data,
        zipcode = form.zipcode.data,
        user_id = 1 #REPLACE WITH ACTUAL USER ID
        )
        event.skills = Skill.query.filter(Skill.id.in_(form.skills.data)).all()
        db.session.add(event)
        db.session.commit()
        flash(f'The Event : {form.name.data} has been successfully created','success')

        form = EventCreateForm()
        
        return redirect(url_for('event_create'))
    return render_template("event-create.html", form=form)

@app.route("/event/<int:event_id>/manage", methods=['GET','POST'])
def event_manage(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventManageForm(obj=event)
    form.state.choices = [(state.id, state.name) for state in State.query.all()]
    form.skills.choices = [(skill.id, skill.name) for skill in Skill.query.all()]

    if request.method == 'GET':
        form.name.data = event.name
        form.description.data = event.description
        form.date.data = event.date
        form.urgency.data = event.urgency
        form.address.data = event.address
        form.city.data = event.city
        form.state.data = event.state
        form.zipcode.data = event.zipcode
        form.skills.data = event.skills
    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        event.date = form.date.data
        event.urgency = form.urgency.data
        event.address = form.address.data
        event.state_id = form.state.data
        event.zipcode = form.zipcode.data
        event.skills = Skill.query.filter(Skill.id.in_(form.skills.data)).all()
        db.session.commit()

        flash(f'The Event : {form.name.data} has been successfully updated','success')
        return redirect(url_for('event_manage', event_id=event_id))

    return render_template("event-manage.html", form=form, event=event, event_id=event_id)





class EventSelectionForm(FlaskForm):
    event_id = HiddenField('Event ID', validators=[DataRequired()])
    submit = SubmitField('Select Event')

class VolunteerSelectionForm(FlaskForm):
    volunteer_id = HiddenField('Volunteer ID', validators=[DataRequired()])
    submit = SubmitField('Select Volunteer')

def match_volunteers_to_events(volunteers, events):
    matches = []
    for event in events:
        required_skills = set(event['required_skills'].split(', '))
        for volunteer in volunteers:
            volunteer_skills = set(volunteer['skills'].split(', '))
            if required_skills.issubset(volunteer_skills):
                matches.append((volunteer, event))
    return matches

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    form = EventSelectionForm()
    if form.validate_on_submit():
        event_id = form.event_id.data
        return redirect(url_for('view_event', event_id=event_id))
    return render_template("adminEvents.html", events=events, form=form)

@app.route("/admin/event/<int:event_id>", methods=['GET', 'POST'])
def view_event(event_id):
    form = VolunteerSelectionForm()
    selected_event = next((event for event in events if event['id'] == event_id), None)
    matches = match_volunteers_to_events(volunteers, events)
    matched_volunteers = [match[0] for match in matches if match[1] == selected_event]
    success_message = None

    if form.validate_on_submit():
        volunteer_id = form.volunteer_id.data
        selected_volunteer = next((v for v in volunteers if str(v['id']) == volunteer_id), None)
        success_message = f'Successfully matched volunteer: {selected_volunteer["name"]} for the event: {selected_event["event_name"]}'

    return render_template("adminMatching.html", event=selected_event, volunteers=matched_volunteers, form=form, success_message=success_message)

@app.route("/volunteer", methods=['GET', 'POST'])
def volunteer():
    form = EventSelectionForm()
    volunteer = volunteers[0]  # Simulating fetching from DB
    matches = match_volunteers_to_events(volunteers, events)
    matched_events = [match[1] for match in matches if match[0] == volunteer]
    success_message = None

    if form.validate_on_submit():
        event_id = form.event_id.data
        selected_event = next((event for event in events if event['id'] == event_id), None)
        success_message = f'Successfully matched with event: {selected_event["event_name"]}'

    return render_template("volunteerMatching.html", volunteer=volunteer, events=matched_events, form=form, success_message=success_message)


@app.route("/history/<int:volunteer_id>")
def history(volunteer_id):
    volunteer = next((v for v in volunteers if v['id'] == volunteer_id), None)
    volunteer_events = [event for event in events if event['volunteer_id'] == volunteer_id]
    return render_template("history.html", volunteer=volunteer, events=volunteer_events)

class PricingModule:
    def __init__(self):
        self.prices = {}

    def set_price(self, item, price):
        self.prices[item] = price

    def get_price(self, item):
        return self.prices.get(item, None)

if __name__ == '__main__': 
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True) # starts server
