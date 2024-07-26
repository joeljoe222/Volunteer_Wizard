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
    name = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Notification', validators=[DataRequired(), Length(max=300)])
    submit = SubmitField('Push Notification')

#make max fit with databses, zipcode requirements can be found in ass.2, make urgency database mayb?
class EventCreateForm(FlaskForm):
    name = StringField('Name of Event', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    date = DateField('Event Date', validators=[DataRequired()])
    urgency = SelectField('Urgency', validators=[DataRequired()], choices=urgencyLevel)
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', coerce=int, validators=[DataRequired()])
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=10)])
    skills = SelectMultipleField('Required Skills', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Event')


class EventManageForm(FlaskForm):
    name = StringField('Name of Event', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    date = DateField('Event Date', validators=[DataRequired()])
    urgency = SelectField('Urgency', validators=[DataRequired()], choices=urgencyLevel)
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField('State', validators=[DataRequired()], choices=state)
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=10)])
    skills = SelectMultipleField('Required Skills', validators=[DataRequired()], choices=skills)
    submit = SubmitField('Update Event')

