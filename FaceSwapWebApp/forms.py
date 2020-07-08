from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

class MainForm(FlaskForm):
	main_file = FileField()
	second_file = FileField()
	submit = SubmitField('Merge Faces')
