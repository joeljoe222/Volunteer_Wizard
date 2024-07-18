from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from forms import NotificationForm, EventCreateForm, EventManageForm
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x8f\xda\xe2o\xfa\x97Qa\xfa\xc1e\xab\xb5z\\f\xf3\x0b\xb9\xa5\xb6\xd7.\xc3'
csrf = CSRFProtect(app)



#TODO LIST for Jay Mejia :
#make event seen from events page and update as edits are made
#do the same with notification page
#change all varibles and functions to snake_case
#change html urls to be event-page
#comment all work

#Example Event
event_data = {
    'eventName':'Example Event',
    'eventDesc':'Here is where an Admin would write a description for the Event',
    'eventDate':datetime.date(2024, 7, 24),
    'urgency':'1',
    'eventAddress':'404 Street Name',
    'country':'USA',
    'state':'TX',
    'zipcode':'11220',
    'requiredSkills':['a','c']
}

#Example Notification
notification_data = {
    'notifName':'Notification Title',
    'notifDesc':'This is where the main notification information will be'
}


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
    return render_template("index.html", volunteers=volunteers)
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
    return render_template("notificationSystem.html")


@app.route("/notification", methods=['GET','POST'])
def notification():
    form = NotificationForm()
    if form.validate_on_submit():
        notification_data['notifName'] = form.notifName.data
        notification_data['notifDesc'] = form.notifDesc.data
        
        flash(f'Notification Sent! : {form.notifName.data} <br> {form.notifDesc.data}','success')
        
        return redirect(url_for('notification'))
    return render_template('notification.html', form=form)

@app.route("/eventCreator", methods=['GET','POST'])
def eventCreator():
    form = EventCreateForm()
    if form.validate_on_submit():
        eventName = form.eventName.data
        eventDesc = form.eventDesc.data
        eventDate = form.eventDate.data
        urgency = form.urgency.data
        eventAddress = form.eventAddress.data
        country = form.country.data
        state = form.state.data
        zipcode = form.zipcode.data
        requiredSkills = form.requiredSkills.data

        flash(f'The Event : {form.eventName.data} has been successfully created','success')

        form = EventCreateForm()
        
        return redirect(url_for('eventCreator'))
    return render_template("eventCreator.html", form=form)

@app.route("/eventManager", methods=['GET','POST'])
def eventManager():
    form = EventManageForm(obj=event_data)
    #form.eventName.data = event_data['eventName']
    if request.method == 'GET':
        form.eventName.data = event_data['eventName']
        form.eventDesc.data = event_data['eventDesc']
        form.eventDate.data = event_data['eventDate']
        form.urgency.data = event_data['urgency']
        form.eventAddress.data = event_data['eventAddress']
        form.country.data = event_data['country']
        form.state.data = event_data['state']
        form.zipcode.data = event_data['zipcode']
        form.requiredSkills.data = event_data['requiredSkills']
    if form.validate_on_submit():
        #form.populate_obj(event_data)
        event_data['eventName'] = form.eventName.data
        event_data['eventDesc'] = form.eventDesc.data
        event_data['eventDate'] = form.eventDate.data
        event_data['urgency'] = form.urgency.data
        event_data['eventAddress'] = form.eventAddress.data
        event_data['country'] = form.country.data
        event_data['state'] = form.state.data
        event_data['zipcode'] = form.zipcode.data
        event_data['requiredSkills'] = form.requiredSkills.data

        flash(f'The Event : {form.eventName.data} has been successfully updated','success')
        return redirect(url_for('eventManager'))
    print("Event Data: ", event_data)
    print("Form Data: ", form.data)

    return render_template("eventManager.html", form=form, event=event_data)

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
