#All forms are found here
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectField, SelectMultipleField, EmailField, PasswordField, HiddenField
from wtforms.validators import DataRequired, Length, Email

#Naming SubjectActionForm()

#===============================================================================
#New User Registration Form
class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[('1', 'Volunteer'), ('2', 'Administrator')], validators=[DataRequired()])
    submit = SubmitField('Submit')

#Existing User Login Form
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


#===============================================================================
#Notification Create Form
class NotificationForm(FlaskForm):
    event_id = HiddenField('Event ID', validators=[DataRequired()])
    name = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Notification', validators=[DataRequired(), Length(max=300)])
    submit = SubmitField('Push Notification')

#make max fit with databses, zipcode requirements can be found in ass.2, make urgency database mayb?
#Event Create Form
class EventCreateForm(FlaskForm):
    name = StringField('Name of Event', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    date = DateField('Event Date', validators=[DataRequired()])
    urgency = SelectField('Urgency', validators=[DataRequired()], choices=['0','1','2','3','4','5'])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', coerce=int, validators=[DataRequired()])
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=10)])
    skills = SelectMultipleField('Required Skills', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Event')

#Event Manage Form
class EventManageForm(FlaskForm):
    name = StringField('Name of Event', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    date = DateField('Event Date', validators=[DataRequired()])
    urgency = SelectField('Urgency', validators=[DataRequired()], choices=['0','1','2','3','4','5'])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', validators=[DataRequired()])
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=10)])
    skills = SelectMultipleField('Required Skills', validators=[DataRequired()])
    submit = SubmitField('Update Event')


#===============================================================================
#Event Selection Form
class EventSelectionForm(FlaskForm):
    event_id = HiddenField('Event ID', validators=[DataRequired()])
    submit = SubmitField('Select Event')

#Volunteer Selection Form
class VolunteerSelectionForm(FlaskForm):
    volunteer_id = HiddenField('Volunteer ID', validators=[DataRequired()])
    submit = SubmitField('Select Volunteer')

