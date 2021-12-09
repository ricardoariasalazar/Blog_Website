from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from email_validator import *
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from website.database import User

# Registration form class
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Check if the user introduced to the database already exists
    def validate_username(self, username):
      user = User.query.filter_by(username=username.data).first() #Find if there is any duplicate user in the database 
      if user:
        raise ValidationError(f'{user.username} is already taken. Try a different one')
    
    # Check if the email introduced to the database already exists
    def validate_email(self, email):
      email = User.query.filter_by(email=email.data).first() #Find if there is any duplicate email in the database 
      if email:
        raise ValidationError(f'{email.email} is already in use. Try a different one')


# Login form class
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Registration form class
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    # Check if the user introduced to the database already exists
    def validate_username(self, username):
      if username.data != current_user.username:
        user = User.query.filter_by(username=username.data).first() #Find if there is any duplicate user in the database 
        if user:
          raise ValidationError(f'{user.username} is already taken. Try a different one')
    
    # Check if the email introduced to the database already exists
    def validate_email(self, email):
      if email.data != current_user.email:
        email = User.query.filter_by(email=email.data).first() #Find if there is any duplicate email in the database 
        if email:
          raise ValidationError(f'{email.email} is already in use. Try a different one')

# Registration form class
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Email()])
  submit = SubmitField('Request Password Reset')

  # Check if the email introduced to the database already exists
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first() #Find if there is any duplicate email in the database 
    if user is None:
      raise ValidationError(f'There is no account with that email. You must register first')

class ResetPasswordForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Reset Password ')
