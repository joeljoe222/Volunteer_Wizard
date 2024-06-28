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
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        skills_selected = request.form.getlist('skills')
        availability = request.form['availability']

        # save to database add later

        return "Profile successfully updated!"
    return render_template("profile.html", states=states, skills=skills)

@app.route("/eventManager")
def eventManager():
    return render_template("eventManager.html");

@app.route("/notificationSystem")
def notificationManager():
    return render_template("notificationSystem.html");

@app.route("/Volunteer matching form")
def volunteerMatching():
    return render_template("volunteer.html")

@app.route("/Admin volunteer matching form")
def adminMatching():
    return render_template("admin.html")

@app.route("/Volunteer history")
def adminMatching():
    return render_template("history.html")

if __name__ == '__main__': app.run(host='0.0.0.0', debug=True) # starts server