from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField,ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')
        
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email is already used before. Please choose a different one.')
    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ReviewForm(FlaskForm):
    review = TextAreaField('Enter your review', validators=[DataRequired()])
    submit = SubmitField('Analyze')



class CSVUploadForm(FlaskForm):
    csv_file = FileField('Upload CSV File', validators=[FileRequired()])
    submit = SubmitField('Analyze')