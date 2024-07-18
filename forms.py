from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length

urgencyLevel = [
    ('','Select Urgency'),
    ('0','Level 0'),
    ('1','Level 1'),
    ('2','Level 2'),
    ('3','Level 3')
]

skills = [
    ('a','Skill 1'),
    ('b','Skill 2'),
    ('c','Skill 3')
]

country = [
    ('','Select Country'),
    ('USA','United States'),
    ('0','Other')
]

state = [
    ('','Select state'),
    ('TX','Texas'),
    ('FL','Florida'),
    ('NY','New York'),
    ('CA','California')
]

#Naming SubjectAction()

class NotificationForm(FlaskForm):
    notifName = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    notifDesc = TextAreaField('Notification', validators=[DataRequired(), Length(max=300)])
    submit = SubmitField('Push Notification')


class EventCreateForm(FlaskForm):
    eventName = StringField('Name of Event', validators=[DataRequired(), Length(min=2, max=100)])
    eventDesc = TextAreaField('Event Description', validators=[DataRequired()])
    eventDate = DateField('Event Date', validators=[DataRequired()])
    urgency = SelectField('Urgency', validators=[DataRequired()], choices=urgencyLevel)
    eventAddress = StringField('Address', validators=[DataRequired()])
    country = SelectField('Country', validators=[DataRequired()], choices=country)
    state = SelectField('State', validators=[DataRequired()], choices=state)
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=10)])
    requiredSkills = SelectMultipleField('Required Skills', validators=[DataRequired()], choices=skills)
    submit = SubmitField('Upload Event')


class EventManageForm(FlaskForm):
    eventName = StringField('Name of Event', validators=[DataRequired(), Length(min=2, max=100)])
    eventDesc = TextAreaField('Event Description', validators=[DataRequired()])
    eventDate = DateField('Event Date', validators=[DataRequired()])
    urgency = SelectField('Urgency', validators=[DataRequired()], choices=urgencyLevel)
    eventAddress = StringField('Address', validators=[DataRequired()])
    country = SelectField('Country', validators=[DataRequired()], choices=country)
    state = SelectField('State', validators=[DataRequired()], choices=state)
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=10)])
    requiredSkills = SelectMultipleField('Required Skills', validators=[DataRequired()], choices=skills)
    submit = SubmitField('Update Event')
