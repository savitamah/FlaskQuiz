from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
 #from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=(DataRequired(), Email()))
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', 
                validators=(DataRequired(), EqualTo('password')))
    submit = SubmitField('Register') 

              #custom validation

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists.')

class QuestionForm(FlaskForm):
    options = RadioField('Options: ', validators=[DataRequired()], default=1)
    submit = SubmitField('Next')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=(DataRequired(), Email()))
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', 
                validators=(DataRequired(), EqualTo('password')))
    submit = SubmitField('Reset Password')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no user with that email.You must register first.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('There is no user with that username.You must register first.')

# class ResetPasswordForm(FlaskForm): 
#     password = PasswordField('Password', validators=[DataRequired()])
#     password2 = PasswordField('Confirm Password', 
#                 validators=(DataRequired(), EqualTo('password')))
#     submit = SubmitField('Reset Password') 

