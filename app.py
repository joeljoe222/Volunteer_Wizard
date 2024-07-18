from flask import Flask, render_template, request, redirect, url_for, flash
from forms import NotificationForm, EventCreateForm, EventManageForm
import datetime

#TODO LIST :
#stallmake event seen from events page and update as edits are made
#do the same with notification page
#change all varibles and functions to snake_case
#change html urls to be event-page
#comment all work

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


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