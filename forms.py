from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, URL, Optional

class OrganizationForm(FlaskForm):
    name = StringField('Organisationsnamn', validators=[DataRequired()])
    description = TextAreaField('Beskrivning', validators=[DataRequired()])
    website = StringField('Webbplats', validators=[Optional(), URL()])
    email = StringField('E-post', validators=[Optional(), Email()])
    phone = StringField('Telefon', validators=[Optional()])
    address = StringField('Adress', validators=[Optional()])
    municipality_id = SelectField('Kommun', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Skicka')
