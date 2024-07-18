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
    notification_name = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    notification_description = TextAreaField('Notification', validators=[DataRequired(), Length(max=300)])
    submit = SubmitField('Push Notification')


class EventCreateForm(FlaskForm):
    event_name = StringField('Name of Event', validators=[DataRequired(), Length(min=2, max=100)])
    event_description = TextAreaField('Event Description', validators=[DataRequired()])
    event_date = DateField('Event Date', validators=[DataRequired()])
    urgency = SelectField('Urgency', validators=[DataRequired()], choices=urgencyLevel)
    event_address = StringField('Address', validators=[DataRequired()])
    event_country = SelectField('Country', validators=[DataRequired()], choices=country)
    event_state = SelectField('State', validators=[DataRequired()], choices=state)
    event_zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=10)])
    required_skills = SelectMultipleField('Required Skills', validators=[DataRequired()], choices=skills)
    submit = SubmitField('Upload Event')


class EventManageForm(FlaskForm):
    event_name = StringField('Name of Event', validators=[DataRequired(), Length(min=2, max=100)])
    event_description = TextAreaField('Event Description', validators=[DataRequired()])
    event_date = DateField('Event Date', validators=[DataRequired()])
    urgency = SelectField('Urgency', validators=[DataRequired()], choices=urgencyLevel)
    event_address = StringField('Address', validators=[DataRequired()])
    event_country = SelectField('Country', validators=[DataRequired()], choices=country)
    event_state = SelectField('State', validators=[DataRequired()], choices=state)
    event_zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=10)])
    required_skills = SelectMultipleField('Required Skills', validators=[DataRequired()], choices=skills)
    submit = SubmitField('Update Event')
