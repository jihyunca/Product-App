from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# A class for the PostalCode form. Contains the item field (product searched for)
# and the submit button
class AddressForm(FlaskForm):
	item = StringField('Enter an Address:', validators=[DataRequired()])
	submit = SubmitField('Search')
