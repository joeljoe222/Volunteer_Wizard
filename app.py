from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x8f\xda\xe2o\xfa\x97Qa\xfa\xc1e\xab\xb5z\\f\xf3\x0b\xb9\xa5\xb6\xd7.\xc3'
csrf = CSRFProtect(app)

# just sample until DB
states = [
    {'code': 'AL', 'name': 'Alabama'},
    {'code': 'AK', 'name': 'Alaska'},
    
]
#sample until DB
skills = [
    'Skill 1', 'Skill 2', 'Skill 3', 'Skill 4', 'Skill 5'
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about") # flask url_for 
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        #save to db here later
       
        return redirect(url_for('profile'))

    return render_template("register.html")

@app.route("/profile", methods=['GET','POST'])
def profile():
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

        return "Profile successfully updated!"
    return render_template("profile.html", states=states, skills=skills)

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


@app.route("/History")
def history():
    return render_template("history.html")

if __name__ == '__main__': app.run(host='0.0.0.0', debug=True) # starts server