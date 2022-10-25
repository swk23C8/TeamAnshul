from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateTimeLocalField, IntegerField, SelectField, DateTimeField, DateTimeField 
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG','JPG','png','jpg'}


#Create new event 
class DestinationForm(FlaskForm):
  name = StringField('Event Name:', validators=[InputRequired()], render_kw={"placeholder": "Name of Event"})
  description = TextAreaField('Description:', validators=[InputRequired()], render_kw={"placeholder": "Name of Event"})
  image = FileField('Event Image:', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
  #Have to change fields and add vars in class in models.py
  ticket_num = IntegerField('Number of Tickets:', validators=[InputRequired(), NumberRange(min=0, max=100)], render_kw={"placeholder": "Number of Available Tickets"})
  ticket_price = IntegerField('Price of Each Ticket:', validators=[InputRequired(), NumberRange(min=0, max=100)], render_kw={"placeholder": "Price Per Ticket (AUD ONLY)"})
  event_date = DateTimeLocalField('When is this Event Happening?', validators=[InputRequired('Enter Time Only')], render_kw={"placeholder": "Offical Start Time and Date"}, format='%Y-%m-%dT%H:%M')
  starting_date = DateTimeLocalField('When are tickets opening?', validators=[InputRequired()], render_kw={"placeholder": "Date of Ticket Release"}, format='%Y-%m-%dT%H:%M')
  closing_date = DateTimeLocalField('When are tickets closing?', render_kw={"placeholder": "Date of Ticket closure"}, validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
  Event_status = SelectField('Event Status:', choices=[('', ''),('Upcoming', 'Upcoming'), ('Inactive', 'Inactive'), ('Booked', 'Booked'), ('Cancelled', 'Cancelled')], render_kw={"placeholder": "Pick an Event Status"}, validators=[InputRequired()])
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
  
  
  
class BookingForm(FlaskForm):
  ticket_num = IntegerField('Number of Tickets:', validators=[InputRequired(), NumberRange(min=0, max=10)], render_kw={"placeholder": "Number of Available Tickets"})
  submit = SubmitField('Book')

  
  
  
#class Updatedestination(FlaskForm):
#  new_destination_name = StringField('New destination Name', validators=[InputRequired])
#  
#  new_description = TextAreaField('Description:', validators=[InputRequired()], render_kw={"placeholder": "Name of Event"})
#  new_image = FileField('New Event Image:', validators=[
#    FileRequired(message='Image cannot be empty'),
#    FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
#  #Have to change fields and add vars in class in models.py
#  new_ticket_num = IntegerField('New Number of Tickets:', render_kw={"placeholder": "Number of Available Tickets"})
#  new_ticket_price = IntegerField('New Price of Each Ticket:', render_kw={"placeholder": "Price Per Ticket (AUD ONLY)"})
#  new_event_date = DateTimeLocalField('New Event Happening Date?', render_kw={"placeholder": "Offical Start Time and Date"}, format='%Y-%m-%dT%H:%M')
#  new_starting_date = DateTimeLocalField('New tickets opening Date:', render_kw={"placeholder": "Date of Ticket Release"}, format='%Y-%m-%dT%H:%M')
#  new_closing_date = DateTimeLocalField('New tickets closing Date:', render_kw={"placeholder": "Date of Ticket closure"}, format='%Y-%m-%dT%H:%M')
#  new_Event_status = SelectField('New Event Status:', choices=[('', ''),('First_choice', 'Upcoming'), ('Second_choice', 'Inactive'), ('Third_choice', 'Booked'), ('forth_choice', 'Cancelled')], render_kw={"placeholder": "Pick an Event Status"})    
#  submit = SubmitField("Update Now")
  