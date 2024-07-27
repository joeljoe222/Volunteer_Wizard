from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import NotificationForm, EventCreateForm, EventManageForm, RegisterForm, LoginForm, EventSelectionForm, VolunteerSelectionForm, VolunteerHistoryForm
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime  
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x8f\xda\xe2o\xfa\x97Qa\xfa\xc1e\xab\xb5z\\f\xf3\x0b\xb9\xa5\xb6\xd7.\xc3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


#Define association for skills - used for matching module possibly?
event_skills = db.Table('event_skills',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'), primary_key=True)
)

#Database Models WIP : Migrate to new file if possible =========================

#User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    #address2 = db.Column(db.String(100))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    skills = db.relationship('Skill', secondary=user_skills, backref=db.backref('users', lazy='dynamic'))
    preferences = db.Column(db.String(200), nullable=False)
    availability = db.Column(db.String(200), nullable=False)
    volunteer_histories = db.relationship('VolunteerHistory', backref='volunteer', lazy=True)


#Volunteer History Model
class VolunteerHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    participation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<VolunteerHistory {self.volunteer_id}-{self.event_id}>'

#Event Model
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

#Notification Model
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

#Skill Model
class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

#State Model
class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    users = db.relationship('User', backref='state', lazy=True)
    events = db.relationship('Event', backref='state', lazy=True)


#All Pages =====================================================================

#Main index page
#Add register button
#Exception thrown when submit
@app.route("/")
def index():
    form = LoginForm()
    return render_template("index.html", form = form)

#About page
#Remake to have info on all teammates and who was in charge of what
@app.route("/about") # flask url_for 
def about():
    return render_template("about.html")

#Test Page : Outputs all Databases Data
#Outputs: SKILL, EVENT, NOTIFICATION, USER
@app.route("/test")
def test_db_output():
    skills = Skill.query.all()
    states = State.query.all()
    users = User.query.all()
    events = Event.query.all()
    notifications = Notification.query.all()
    return render_template("test.html", skills=skills, states=states, users=users, events=events, notifications=notifications)


#User Profile System -----------------------------------------------------------

#Login Page
#What does this page do? Method Not Allowed error
@app.route("/login", methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data # password recived from form/html.file
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password): #check_password_hash(pwhash, password)
            session['email'] = email
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for('profile', email=email))
        else:
            flash("Invalid email or password.", "danger")
    
    return render_template("index.html", form=form)


#Register Page
#Exception thrown when submit
@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit(): #validating
        hashed_password = generate_password_hash(form.password.data ) #method='sha256'

        
        new_user = User(
            name='',
            email=form.email.data,
            password=hashed_password,  
            role=form.role.data,
            address='',
            state_id=1,
            skills=[],
            preferences='',
            availability=''
        )
        db.session.add(new_user)
        db.session.commit()

        flash("User added, please finish setting up")
        return redirect(url_for('profile',email=form.email.data))

    return render_template("register.html", form=form)

#Profile page
#Use profile id rather than email for url
#How to get to this page? name error thrown
@app.route("/profile/<email>", methods=['GET', 'POST'])
def profile(email):
    user = User.query.filter_by(email=email).first()
    states = State.query.all()
    skills = Skill.query.all()

    # captures data entered from profile.html
    if request.method == 'POST':
        user.name = request.form['full_name']
        user.address = f"{request.form['address1']} {request.form['address2']}, {request.form['city']}, {request.form['state_id']}, {request.form['zip_code']}"
        user.state_id = request.form['state_id']
        user.skills = Skill.query.filter(Skill.id.in_(request.form.getlist('skills[]'))).all()
        user.preferences = request.form['preferences']
        user.availability = ', '.join(request.form.getlist('availability[]'))
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('index'))
   
    return render_template("profile.html", states=states, skills=skills, email=email)


#Notification System -----------------------------------------------------------

#Main notification page
#Make Updates only display most recent notification from each event
@app.route("/notification")
def notification_main():
    notifications = Notification.query.all()
    return render_template("notification-main.html", notifications=notifications)

#Create notification page
#Have a notification create for an event id and flash to the event page with the new notification displaying
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


#Event System ------------------------------------------------------------------

#Main event page
#Complete?
@app.route("/event")
def event_main():
    events = Event.query.all()
    return render_template("event-main.html", events=events)

#Event page for specified event
#Complete?
@app.route("/event/<int:event_id>")
def event_view(event_id):
    event = Event.query.get_or_404(event_id)
    notifications = Notification.query.filter_by(event_id=event_id).all()
    return render_template("event-view.html", event=event, event_id=event_id, notifications=notifications)

#Create event page
#Make it accessible to admins only
#Once submitted flash to the new event page
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

#Event management page
#Make it only accessible to Admins
#Skills dont display
#Return to event view page once submit with flash message
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



#Admin and Volunteer Systems ===================================================

#Comment what wach route is

#Admin page
#You can use events page to format this page to show all events
@app.route("/admin")
def admin():
    form = EventSelectionForm()
    events = Event.query.all()  # Fetching all events from the database
    if form.validate_on_submit():
        event_id = form.event_id.data
        return redirect(url_for('view_event', event_id=event_id))
    return render_template("adminEvents.html", events=events, form=form)

#Same route to this page as above? mistake maybe
@app.route("/admin")
def admin_dashboard():
    events = Event.query.all()
    return render_template("adminEvents.html", events=events)

#Undefined error and how would one get to this page normally?
@app.route("/admin/events")
def admin_events():
    events = Event.query.all()
    return render_template("adminEvents.html", events=events)

#this can also be formatted like event_view page showing volunteers instead of notifications
@app.route("/admin/event/<int:event_id>", methods=['GET', 'POST'])
def admin_match(event_id):
    event = Event.query.get_or_404(event_id)
    volunteers = User.query.filter_by(role='volunteer').all()  # Fetch volunteers
    form = VolunteerSelectionForm()

    if form.validate_on_submit():
        volunteer_id = form.volunteer_id.data
        volunteer = User.query.get(volunteer_id)
        if volunteer:
            history = VolunteerHistory(volunteer_id=volunteer.id, event_id=event.id, status='Assigned')
            db.session.add(history)
            db.session.commit()
            flash(f'Volunteer {volunteer.name} assigned to event {event.name}!', 'success')
            return redirect(url_for('admin_match', event_id=event.id))

    return render_template("adminMatching.html", event=event, volunteers=volunteers, form=form)

#Missing Label
#Same route as above?
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

#Volunteer Page
#good job on the flash btw
#Unfinished
@app.route("/volunteer", methods=['GET', 'POST'])
def volunteer():
    form = EventSelectionForm()
    volunteers = User.query.filter_by(role='volunteer').all()  # Fetching all volunteers with role 'volunteer'
    
    # Check if volunteers list is empty
    if not volunteers:
        flash("No volunteers found.", "warning")
        return render_template("volunteerMatching.html", volunteer=None, events=[], form=form)

    volunteer = volunteers[0]  # Simulating fetching the first volunteer
    events = Event.query.all()  # Fetching all events
    matched_events = []  # Replace with logic to get matched events if applicable

    if form.validate_on_submit():
        event_id = form.event_id.data
        selected_event = Event.query.get(event_id)
        success_message = f'Successfully matched with event: {selected_event.name}'
        return render_template("volunteerMatching.html", volunteer=volunteer, events=matched_events, form=form, success_message=success_message)

    return render_template("volunteerMatching.html", volunteer=volunteer, events=matched_events, form=form)

#volunteer dashboard
#Will you also display volunteer history here?
@app.route("/volunteer/<int:volunteer_id>")
def volunteer_dashboard(volunteer_id):
    volunteer = User.query.get_or_404(volunteer_id)
    history = VolunteerHistory.query.filter_by(volunteer_id=volunteer.id).all()
    events = [h.event for h in history if h.event]  # List of events the volunteer is assigned to
    return render_template("volunteerMatching.html", volunteer=volunteer, events=events)

#Volunteer's history page
#Can this just be displayed in route above? or will above site displayed only recent events and this show full history?
@app.route("/history/<int:volunteer_id>")
def history(volunteer_id):
    volunteer = User.query.get_or_404(volunteer_id)
    history = VolunteerHistory.query.filter_by(volunteer_id=volunteer.id).all()
    return render_template("history.html", volunteer=volunteer, history=history)

#no template found
#What would this page do? like an admin would confirm a volunteers participation in an event?
@app.route('/history/add', methods=['GET', 'POST'])
def add_history():
    form = VolunteerHistoryForm()
    if form.validate_on_submit():
        history_record = VolunteerHistory(
            volunteer_id=form.volunteer_id.data,
            event_id=form.event_id.data,
            participation_date=form.participation_date.data,
            status=form.status.data
        )
        db.session.add(history_record)
        db.session.commit()
        flash('Volunteer history added successfully!', 'success')
        return redirect(url_for('history', volunteer_id=form.volunteer_id.data))
    return render_template('add_history.html', form=form)
#End of pages ==================================================================


#match volunteers to events
def match_volunteers_to_events(volunteers, events):
    matches = []
    for event in events:
        required_skills = set(event['required_skills'].split(', '))
        for volunteer in volunteers:
            volunteer_skills = set(volunteer['skills'].split(', '))
            if required_skills.issubset(volunteer_skills):
                matches.append((volunteer, event))
    return matches

#Place holder for Pricing Module
class PricingModule:
    def __init__(self):
        self.prices = {}

    def set_price(self, item, price):
        self.prices[item] = price

    def get_price(self, item):
        return self.prices.get(item, None)


#Runs server locally ===========================================================
#Debug=True allows site to update as it detects changes in these files
#Updating py files will crash server
#Updating html files will show changes on page refresh 
if __name__ == '__main__': 
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
