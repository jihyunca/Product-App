from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# A class for the Search form. Contains the item field (product searched for)
# and the submit button
class ProductSearch(FlaskForm):
	item = StringField('Enter a Product:', validators=[DataRequired()])
	submit = SubmitField('Search')

