from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, StringField, PasswordField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.csrf import CSRFProtect
from forms import NotificationForm, EventCreateForm, EventManageForm
import datetime
# >>>>>>> main

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x8f\xda\xe2o\xfa\x97Qa\xfa\xc1e\xab\xb5z\\f\xf3\x0b\xb9\xa5\xb6\xd7.\xc3'



#TODO LIST for Jay Mejia :
#make NOTIFICATIONS seen from notification page and update as more are added
#make any event manage or view page with no index redirect to event page and flash error

#I AM IN THE MIDDLE OF:
#finished events pages and pushing a commit

#Clarify and cleaning up code : This is a suggestion just to clean up our code and maintain readability, these are based of suggestions for each language
#Do not abbreviate and comment your code
#   Python:
#       change all variables and functions to snake_case
#       change all classes to CamelCase
#       constants are capatilized MAX_ATTEMPTS
#   HTML:
#       change URLs to use dashes event-main, event-create



#HARDCODED DATA FOR ASSIGNMENT 3

#Example Event
event_data = {
    1 : {
        'event_name':'Example Event One',
        'event_description':'Description for Event One',
        'event_date':datetime.date(2025, 1, 1),
        'urgency':'1',
        'event_address':'1111 Street Name',
        'event_country':'USA',
        'event_state':'TX',
        'event_zipcode':'11111',
        'required_skills':['a']
    },
    2 : {
        'event_name':'Example Event Two',
        'event_description':'Description for Event Two',
        'event_date':datetime.date(2025, 2, 2),
        'urgency':'2',
        'event_address':'2222 Street Name',
        'event_country':'USA',
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
    'notification_name':'Notification Title',
    'notification_description':'This is where the main notification information will be'
}


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

#All pages involved in Application

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
#>>>>>>> main

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


#NOTIFICATION SYSTEM -----------------------------------------------------------
@app.route("/notification-main")
def notification_main():
    return render_template("notification-main.html")


@app.route("/notification-create", methods=['GET','POST'])
def notification_create():
    form = NotificationForm()
    if form.validate_on_submit():
        notification_data['notification_name'] = form.notification_name.data
        notification_data['notification_description'] = form.notification_description.data
        
        flash(f'Notification Sent! : {form.notification_name.data} <br> {form.notification_description.data}','success')
        
        return redirect(url_for('notification_create'))
    return render_template('notification-create.html', form=form)


#EVENT SYSTEM ------------------------------------------------------------------
@app.route("/event")
def event_main():
    return render_template("event-main.html", event_data=event_data, skill_data=skill_data)

@app.route("/event/create", methods=['GET','POST'])
def event_create():
    form = EventCreateForm()
    if form.validate_on_submit():
        event_name = form.event_name.data
        event_description = form.event_description.data
        event_date = form.event_date.data
        urgency = form.urgency.data
        event_address = form.event_address.data
        event_country = form.event_country.data
        event_state = form.event_state.data
        event_zipcode = form.event_zipcode.data
        required_skills = form.required_skills.data

        flash(f'The Event : {form.event_name.data} has been successfully created','success')

        form = EventCreateForm()
        
        return redirect(url_for('event_create'))
    return render_template("event-create.html", form=form)

@app.route("/event/<int:event_id>/manage", methods=['GET','POST'])
def event_manage(event_id):
    event = event_data.get(event_id)
    form = EventManageForm(obj=event)
    #form.event_name.data = event_data['event_name']
    if request.method == 'GET':
        form.event_name.data = event['event_name']
        form.event_description.data = event['event_description']
        form.event_date.data = event['event_date']
        form.urgency.data = event['urgency']
        form.event_address.data = event['event_address']
        form.event_country.data = event['event_country']
        form.event_state.data = event['event_state']
        form.event_zipcode.data = event['event_zipcode']
        form.required_skills.data = event['required_skills']
    if form.validate_on_submit():
        #form.populate_obj(event_data)
        event['event_name'] = form.event_name.data
        event['event_description'] = form.event_description.data
        event['event_date'] = form.event_date.data
        event['urgency'] = form.urgency.data
        event['event_address'] = form.event_address.data
        event['event_country'] = form.event_country.data
        event['event_state'] = form.event_state.data
        event['event_zipcode'] = form.event_zipcode.data
        event['required_skills'] = form.required_skills.data

        flash(f'The Event : {form.event_name.data} has been successfully updated','success')
        return redirect(url_for('event_manage', event_id=event_id))
    #print("Event Data: ", event_data)
    #print("Form Data: ", form.data)

    return render_template("event-manage.html", form=form, event=event, event_id=event_id)

@app.route("/event/<int:event_id>")
def event_view(event_id):
    event = event_data.get(event_id)
    if event is None:
        abort(404) #Update to redirect to event not found page with a link back to event-main
    return render_template("event-view.html", event=event, event_id=event_id, skill_data=skill_data)



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

if __name__ == '__main__': app.run(host='0.0.0.0', debug=True) # starts server
