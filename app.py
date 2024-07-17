from flask import Flask, render_template, request, redirect, url_for, flash
from forms import NotificationForm, EventForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

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
        notifName = form.notifName.data
        notifDesc = form.notifDesc.data
        
        flash(f'Notification Sent! : {form.notifName.data} <br> {form.notifDesc.data}','success')
        
        return redirect(url_for('notification'))
    else:
        print('notif failed validation')
        print(form.errors)
    return render_template('notification.html', form=form)

@app.route("/eventManager", methods=['GET','POST'])
def eventManager():
    form = EventForm()
    if form.validate_on_submit():
        print('Event Form Validated')

        eventName = form.eventName.data
        eventDesc = form.eventDesc.data
        eventDate = form.eventDate.data
        urgency = form.urgency.data
        eventAddress = form.eventAddress.data
        country = form.country.data
        state = form.state.data
        zipcode = form.zipcode.data
        requiredSkills = form.requiredSkills.data

        flash(f'The Event : {form.eventName.data} has been successfully updated','success')
        
        print('Event Flash')

        form = EventForm()
        
        return redirect(url_for('eventManager'))
    else:
        print('Event did NOT validate')
        print(form.errors)
    return render_template("eventManager.html", form=form)

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