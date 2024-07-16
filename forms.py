from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class NotificationForm(FlaskForm):
    notifName = StringField('Title', validators=[DataRequired(), Length(min=2, max=50)])
    notifDesc = TextAreaField('Notification', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Submit')
