from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from forms import NotificationForm, EventCreateForm, EventManageForm, RegisterForm, LoginForm, EventSelectionForm, VolunteerSelectionForm, VolunteerHistoryForm 
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, VolunteerHistory, Event, Notification, Skill, State
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
import csv
from io import BytesIO, StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



app = Flask(__name__)
app.config['SECRET_KEY'] = b'\x8f\xda\xe2o\xfa\x97Qa\xfa\xc1e\xab\xb5z\\f\xf3\x0b\xb9\xa5\xb6\xd7.\xc3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
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

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('about'))

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
@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if user.role == 'admin':
                return redirect(next_page or url_for('admin'))
            elif user.role == 'volunteer':
                return redirect(next_page or url_for('volunteer_dashboard', volunteer_id=user.id))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("login.html", form=form)


#Register Page
#Exception thrown when submit
@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit(): #validating
        email = form.email.data
        # Check if email already exists
        
        user = User.query.filter_by(email=email).first()
        if user:
            # Email already exists
            flash("Email is already registered. Please use a different email or Log in", "danger")
            return render_template("register.html", form=form)
         #method='sha256'
        
        hashed_password = generate_password_hash(form.password.data )
        new_user = User(
            name='',
            email=email,
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
@login_required
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
   
    return render_template("profile.html", user=user, states=states, skills=skills)

#admin required page management 
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        if current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/manage_users', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_users():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        return redirect(url_for('manage_users'))
    
    users = User.query.all()
    return render_template('manage_users.html', users=users)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('manage_users'))


#Notification System -----------------------------------------------------------

#Main notification page
@app.route("/notification")
def notification_main():
    notifications = Notification.query.all()
    events = Event.query.all()

    notifications_in_event = {}
    latest_notification_in_event = {}

    for event in events:
        notifications_in_event[event.id] = [notification for notification in notifications if notification.event_id == event.id]
        latest_notification = Notification.query.filter_by(event_id=event.id).order_by(Notification.id.desc()).first()
        if latest_notification:
            latest_notification_in_event[event.id] = latest_notification

    return render_template("notification-main.html", notifications=notifications, events=events, notifications_in_event=notifications_in_event, latest_notification_in_event=latest_notification_in_event)

#Create notification page
@app.route("/notification/create/<int:event_id>", methods=['GET','POST'])
def notification_create(event_id):
    form = NotificationForm()
    
    if request.method == 'GET':
        form.event_id.data = event_id
    if form.validate_on_submit():
        notification = Notification(
            name = form.name.data,
            description = form.description.data,
            event_id = form.event_id.data
        )
        db.session.add(notification)
        db.session.commit()
        flash(f'Notification Sent! : {form.name.data}','success')
        
        return redirect(url_for('notification_create', event_id=event_id))
    return render_template('notification-create.html', form=form, event_id=event_id)

@app.route("/notification/manage/<int:event_id>/<int:notification_id>", methods=['GET','POST'])
def notification_manage(event_id,notification_id):
    event = Event.query.get_or_404(event_id)
    notification = Notification.query.filter_by(event_id=event_id, id=notification_id).first()
    form = NotificationForm(obj=notification)

    if request.method == 'GET':
        form.name.data = notification.name
        form.description.data = notification.description
    if form.validate_on_submit():
        notification.name = form.name.data
        notification.description = form.description.data
        db.session.commit()
        flash(f'Notification : {notification.name} succesfully updated!','success')
        return redirect(url_for('event_view', event_id=event_id))
    return render_template('notification-manage.html', form=form,event_id=event_id, notification_id=notification_id, event=event, notification=notification)

@app.route("/notification/delete/<int:event_id>/<int:notification_id>", methods=['POST','GET'])
def notification_delete(event_id,notification_id):
    notification = Notification.query.filter_by(event_id=event_id, id=notification_id).first()

    if session['role'] != 'admin':
        flash('You do not have permission to delete this notification.', 'danger')
        return redirect(url_for('event_view',event_id=event_id))
    try:
        db.session.delete(notification)
        db.session.commit()
        flash('Notification deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while trying to delete the notification.', 'danger')
        print(f"Error: {e}")
    return redirect(url_for('event_view',event_id=event_id))



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
        form.skills.data = [skill.id for skill in event.skills]
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

@app.route("/event/delete/<int:event_id>", methods=['POST','GET'])
def event_delete(event_id):
    event = Event.query.get_or_404(event_id)
    notifications = Notification.query.filter_by(event_id=event_id).all()
    if session['role'] != 'admin':
        flash('You do not have permission to delete this notification.', 'danger')
        return redirect(url_for('event_view',event_id=event_id))
    try:
        for notification in notifications:
            db.session.delete(notification)
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while trying to delete the event.', 'danger')
        print(f"Error: {e}")
    return redirect(url_for('event_main'))

#Admin and Volunteer Systems ===================================================

#Comment what wach route is

# Admin page to view all events and assign volunteers
@app.route("/admin")
@login_required
@admin_required
def admin():
    events = Event.query.all()
    return render_template("adminEvents.html", events=events)

# Admin page to match volunteers to a specific event
@app.route("/admin/event/<int:event_id>", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_match(event_id):
    event = Event.query.get_or_404(event_id)
    volunteers = User.query.filter_by(role='volunteer').all()
    form = VolunteerSelectionForm()

    if form.validate_on_submit():
        volunteer_id = form.volunteer_id.data
        history = VolunteerHistory(volunteer_id=volunteer_id, event_id=event_id, status='In Progress')
        db.session.add(history)
        db.session.commit()
        flash('Volunteer assigned to event!', 'success')
        return redirect(url_for('admin_match', event_id=event_id))

    return render_template("adminMatching.html", event=event, volunteers=volunteers, form=form)

# Volunteer dashboard to view assigned events
@app.route("/volunteer/<int:volunteer_id>")
@login_required
def volunteer_dashboard(volunteer_id):
    volunteer = User.query.get_or_404(volunteer_id)
    history = VolunteerHistory.query.filter_by(volunteer_id=volunteer.id).all()
    events = [h.event for h in history if h.event]
    return render_template("volunteerMatching.html", volunteer=volunteer, events=events)

# Volunteer's history page to show event participation status
@app.route("/history/<int:volunteer_id>")
@login_required
def history(volunteer_id):
    volunteer = User.query.get_or_404(volunteer_id)
    history_records = VolunteerHistory.query.filter_by(volunteer_id=volunteer.id).all()
    return render_template("history.html", volunteer=volunteer, history=history_records)

# Route to update volunteer participation status
@app.route("/history/update_status/<int:record_id>", methods=['POST'])
@login_required
def update_status(record_id):
    history_record = VolunteerHistory.query.get_or_404(record_id)
    if history_record.volunteer_id != current_user.id:
        flash('You do not have permission to update this record.', 'danger')
        return redirect(url_for('history', volunteer_id=current_user.id))

    history_record.status = request.form.get('status', 'In Progress')
    db.session.commit()
    flash('Participation status updated!', 'success')
    return redirect(url_for('history', volunteer_id=current_user.id))

# Route to view volunteer history (for admin)
@app.route('/admin/volunteer_history/<int:volunteer_id>')
@login_required
@admin_required
def admin_volunteer_history(volunteer_id):
    volunteer = User.query.get_or_404(volunteer_id)
    history_records = VolunteerHistory.query.filter_by(volunteer_id=volunteer.id).all()
    return render_template("admin_volunteer_history.html", volunteer=volunteer, history=history_records)

# Route to display the admin reports page
@app.route('/admin/reports')
@login_required
@admin_required
def admin_reports():
    return render_template('adminReports.html')

# Route to generate volunteer participation history report in CSV
@app.route('/reports/volunteer_history/csv/<int:volunteer_id>', methods=['GET'])
@login_required
@admin_required
def volunteer_history_csv(volunteer_id):
    volunteer = User.query.get_or_404(volunteer_id)
    history = VolunteerHistory.query.filter_by(volunteer_id=volunteer.id).all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Volunteer Name', 'Event Name', 'Event Description', 'Participation Date', 'Status'])

    for record in history:
        event = Event.query.get(record.event_id)
        cw.writerow([volunteer.name, event.name, event.description, record.participation_date, record.status])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename={volunteer.name}_history.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# Route to generate volunteer participation history report in PDF
@app.route('/reports/volunteer_history/pdf/<int:volunteer_id>', methods=['GET'])
@login_required
@admin_required
def volunteer_history_pdf(volunteer_id):
    volunteer = User.query.get_or_404(volunteer_id)
    history = VolunteerHistory.query.filter_by(volunteer_id=volunteer.id).all()
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica", 12)
    p.drawString(100, height - 40, f"{volunteer.name}'s Participation History Report")

    y = height - 80
    for record in history:
        event = Event.query.get(record.event_id)
        p.drawString(50, y, "Event Name")
        p.drawString(200, y, "Event Description")
        p.drawString(350, y, "Participation Date")
        p.drawString(450, y, "Status")
        y -= 20
        p.drawString(50, y, event.name)
        p.drawString(200, y, event.description)
        p.drawString(350, y, record.participation_date.strftime("%Y-%m-%d %H:%M:%S"))
        p.drawString(450, y, record.status)
        y -= 20
        if y < 100:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = height - 40

    p.save()
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename={volunteer.name}_history.pdf'
    response.headers['Content-Type'] = 'application/pdf'
    return response

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
