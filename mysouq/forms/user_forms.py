from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import InputRequired, EqualTo


class SignUpForm(FlaskForm):
    username = StringField("Username: ", [validators.InputRequired()])
    password = PasswordField("Password: ", [validators.InputRequired()])
    email = EmailField("Email: ", [validators.InputRequired()])
    birthday = DateField("Birthday: ", [validators.InputRequired()], format='%Y-%m-%d')
    submit = SubmitField("SignUp")    


class LoginForm(FlaskForm):
    username = StringField("Username: ", [validators.InputRequired()])
    password = PasswordField("Password: ", [validators.InputRequired()])
    submit = SubmitField("Login")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Enter your current password: ', [InputRequired()])
    new_password = PasswordField('Enter your new password: ', [InputRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField("Confirm your new password: ", [InputRequired()])
    change_password = SubmitField("Change Password")


class EditProfileForm(FlaskForm):
    username = StringField("Username: ", [validators.InputRequired()])
    email = EmailField("Email: ", [validators.InputRequired()])
    birthday = DateField("Birthday: ", [validators.InputRequired()], format='%Y-%m-%d')
    submit = SubmitField("Update Profile") 