from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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