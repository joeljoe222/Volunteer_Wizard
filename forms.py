from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class NotificationForm(FlaskForm):
    notifName = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    notifDesc = TextAreaField('Notification', validators=[DataRequired(), Length(max=300)])
    submit = SubmitField('Push Notification')

class EventForm(FlaskForm):
    eventName = StringField('Name of Event', validators=[DataRequired(), Length(min=2, max=100)])
    eventDesc = TextAreaField('Event Description', validators=[DataRequired()])
    eventDate = DateField('Event Date', validators=[DataRequired()])
    urgency = SelectField('Urgency', validators=[DataRequired()], 
        choices=[
            ('0','Level 0'),
            ('1','Level 1'),
            ('2','Level 2'),
            ('3','Level 3')
        ])
    eventAddress = StringField('Address', validators=[DataRequired()])
    country = SelectField('Country', validators=[DataRequired()], choices= [('USA','United States')])
    state = SelectField('State', validators=[DataRequired()],
        choices=[
            ('TX','Texas'),
            ('FL','Florida')
        ])
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=10)])
    requiredSkills = SelectMultipleField('Required Skills', validators=[DataRequired()], 
        choices=[
            ('skill1','Skill 1'),
            ('skill2','Skill 2'),
            ('skill3','Skill 3')
        ])
    submit = SubmitField('Update Event')
