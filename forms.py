from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class ClueForm(Form):
    question = StringField('Question', validators=[
        DataRequired()
    ])
    answer = StringField('Answer', validators=[
        DataRequired()
    ])
    value = IntegerField('Value', validators=[
        DataRequired()
    ])