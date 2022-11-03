from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__='users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    Contact_num = db.Column(db.String(50), index=True, nullable=False)
    Address = db.Column(db.String(50), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    
    # User can have many posts
    posts = db.relationship('Destination', backref='poster')


#Destinations represents Events
class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    # Name can be taken out ; 'author'
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    #Additional fields neccessary to store in events db
    ticket_num = db.Column(db.Integer())
    ticket_price = db.Column(db.Integer())
    event_date = db.Column(db.DateTime)
    starting_date = db.Column(db.DateTime)
    closing_date = db.Column(db.DateTime)
    Event_status = db.Column(db.String(100))
    
    # Foreign Key to Lnk Users (refer to primary)
    #Reason why user is lower cased is due to it being actually referred to the db. 
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='destination')
    

    def __repr__(self): #string print method
        return "<Name: {}>".format(self.name)
    
    
class Booking(db.Model):
    __tablename__ = 'bookings'
    event_id = db.Column(db.Integer, primary_key=True)
    event_price = db.Column(db.Integer())
    event_qty = db.Column(db.Integer())
    event_booking_date = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))


    def __repr__(self):
        return "<Comment: {}>".format(self.text)