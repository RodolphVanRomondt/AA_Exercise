from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField, validators

class AddUser(FlaskForm):
    """ Form for adding users. """

    username = StringField("Username", [validators.Length(max=20), validators.InputRequired()])

    password = PasswordField("Password", [validators.InputRequired()])
    
    email = EmailField("Email", [validators.Length(max=50), validators.InputRequired()])
    
    first_name = StringField("Firstname", [validators.Length(max=30), validators.InputRequired()])
    
    last_name = StringField("Lastname", [validators.Length(max=30), validators.InputRequired()])

class LoginUser(FlaskForm):
    """ Form for logging users. """

    username = StringField("Username", [validators.InputRequired()])

    password = PasswordField("Password", [validators.InputRequired()])

class FeedbackForm(FlaskForm):
    """ Form for giving feedback. """

    title = StringField("Title", [validators.Length(max=100), validators.InputRequired()])
    content = TextAreaField("Content", [validators.InputRequired()])