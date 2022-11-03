from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateTimeLocalField, IntegerField, SelectField, DateTimeField, DateTimeField 
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG','JPG','png','jpg'}


#Create new event 
class DestinationForm(FlaskForm):
  name = StringField('Event Name:', validators=[InputRequired()], render_kw={"placeholder": "Name of Event"})
  description = TextAreaField('Description:', validators=[InputRequired()], render_kw={"placeholder": "Description of Event"})
  image = FileField('Event Image:', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])
  #Have to change fields and add vars in class in models.py
  ticket_num = IntegerField('Number of Tickets:', validators=[InputRequired(), NumberRange(min=0, max=25000)], render_kw={"placeholder": "Number of Available Tickets"})
  ticket_price = IntegerField('Price of Each Ticket:', validators=[InputRequired(), NumberRange(min=0, max=500)], render_kw={"placeholder": "Price Per Ticket (AUD ONLY)"})
  event_date = DateTimeLocalField('When is this Event Happening?', validators=[InputRequired('Enter Time Only')], render_kw={"placeholder": "Offical Start Time and Date"}, format='%Y-%m-%dT%H:%M')
  starting_date = DateTimeLocalField('When are tickets opening?', validators=[InputRequired()], render_kw={"placeholder": "Date of Ticket Release"}, format='%Y-%m-%dT%H:%M')
  closing_date = DateTimeLocalField('When are tickets closing?', render_kw={"placeholder": "Date of Ticket closure"}, validators=[InputRequired()], format='%Y-%m-%dT%H:%M')
  Event_status = SelectField('Event Status:', choices=[('', ''),('Open', 'Open'), ('Unpublished', 'Unpublished'), ('Sold-out', 'Sold-out'), ('Cancelled', 'Cancelled')], render_kw={"placeholder": "Pick an Event Status"}, validators=[InputRequired()])
  submit = SubmitField("Create")
  
  
#User login
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()], render_kw={"placeholder": "Ex. Example123"})
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")], render_kw={"placeholder": "Ex. LisaisCool@example.com.au"})
    contact_num=StringField("Phone Number", validators=[InputRequired()], render_kw={"placeholder": "Ex. 0434 484 911"})
    address=StringField("Address", validators=[InputRequired()], render_kw={"placeholder": "Ex. Brisbane City, George Street"})
    
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
  ticket_num = IntegerField('Number of Tickets:', validators=[InputRequired(), NumberRange(min=0, max=1000)], render_kw={"placeholder": "Number of Available Tickets"})
  submit = SubmitField('Book')

  

  