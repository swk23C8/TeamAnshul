from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG','JPG','png','jpg'}

#Create new destination
class DestinationForm(FlaskForm):
  name = StringField('Name:', validators=[InputRequired()])
  description = TextAreaField('Description:', 
            validators=[InputRequired()])
  image = FileField('Event Image:', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
  currency = StringField('Currency', validators=[InputRequired()])
  #Have to change fields and add vars in class in models.py
  #ticket_num = StringField('Number of Tickets:', validators=[InputRequired()])
  #ticket_Price = StringField('Price of Each Ticket:', validators=[InputRequired()])
  #event_date = StringField('When is this Event Happening?', validators=[InputRequired()])
  #starting_date = StringField('When are tickets opening?', validators=[InputRequired()])
  #closing_date = StringField('When are tickets closing?', validators=[InputRequired()])
  submit = SubmitField("Create")
    
#User login
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')