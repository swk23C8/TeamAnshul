from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Destination, Comment, Booking
from .forms import DestinationForm, CommentForm, BookingForm
from . import db, app
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user
from flask.json import jsonify

bp = Blueprint('destination', __name__, url_prefix='/events')

@bp.route('/<id>')
def show(id):
    destination = Destination.query.filter_by(id=id).first()
    # create the comment form
    cform = CommentForm()    
    return render_template('destinations/show.html', destination=destination, form=cform)
@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = DestinationForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path=check_upload_file(form)
    
    
    
    destination=Destination(name=form.name.data,
    description=form.description.data, 
    image=db_file_path
    ,ticket_num=form.ticket_num.data
    ,ticket_price=form.ticket_price.data
    ,event_date=form.event_date.data
    ,starting_date=form.starting_date.data
    ,closing_date=form.closing_date.data
    ,Event_status=form.Event_status.data
    ,poster=current_user)
        

    # add the object to the db session
    db.session.add(destination)
    
    # commit to the database
    db.session.commit()
    print('Successfully created new travel destination', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('destination.create'))
  return render_template('destinations/create.html', form=form)

def check_upload_file(form):
  #get file data from form  
  fp=form.image.data
  filename=fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH=os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path=os.path.join(BASE_PATH,'static/img',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path='/static/img/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@bp.route('/<destination>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(destination):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    destination_obj = Destination.query.filter_by(id=destination).first()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        destination=destination_obj,
                        user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('destination.show', id=destination))
  
  
  
#Create Booking for user    
@bp.route('/booking/<destination>', methods = ['GET', 'POST'])  
@login_required
def booking(destination):
  message = None
  form = BookingForm()  
  #get the destination object associated to the page and the booking
  destination_obj = Destination.query.filter_by(id=destination).first().id
  destination_tickets_price = Destination.query.filter_by(id=destination).first().ticket_price
  destination_tickets_remaining = Destination.query.filter_by(id=destination).first().ticket_num
  #Check if vars are running through
  print(destination_obj)
  print(current_user.id)
  print(destination_tickets_remaining)
  print(destination_tickets_price)

  if form.validate_on_submit():
    
    if form.ticket_num.data > destination_tickets_remaining:
        flash("You've exceeded the number of tickets which are available for this event")
    
    elif destination_tickets_remaining == 0:
        flash("Oh no, you're too late! All tickets are sold out :(")
        db.session.query(Destination).filter(Destination.id == destination).\
          update({'Event_status': 'Sold-out'})
          # Update Event_status to sold-out doesnt work :(
      
    else:
      #read the Booking from the form
      booking = Booking(event_qty=form.ticket_num.data,
                        destination_id = destination_obj,
                        user_id = current_user.id,
                        event_price = destination_tickets_price,
                        )
      db.session.query(Destination).filter(Destination.id == destination).\
        update({'ticket_num': destination_tickets_remaining - form.ticket_num.data})
        
      db.session.add(booking) 
      db.session.commit()
      print("Your Booking has been added") 
  if message != None:
    print(message)
    flash(message)
  # using redirect sends a GET request to destination.show
  return render_template('booking.html', form=form)
    


  
  
  # Deleting the destination
@bp.route('/delete/<int:id>', methods = ['GET','DELETE'])
@login_required
def delete_show(id):
  post_to_delete = Destination.query.get_or_404(id).id
  id = current_user.id

  if id == post_to_delete:

    destination = Destination.query.filter_by(id=id).first()
    # create the comment form
    db.session.delete(destination)
    db.session.commit()
    # Notify User and redirect them back to the main page.
    #flash("Event has been deleted.")
    return redirect(url_for('main.index'))
    

  else:
      return jsonify(message='To delete this, you must be the creator of this Event.'), 200

# Updating the event 
@bp.route('/edit/<int:id>', methods = ['GET','POST'])
@login_required
def edit_post(id):
  
  post_to_delete = Destination.query.get_or_404(id).id
  id = current_user.id
  print(id)
  print(post_to_delete)
  if id == post_to_delete:
    post = Destination.query.get_or_404(id)
    form = DestinationForm()
    if form.validate_on_submit():
      post.name = form.name.data
      db_file_path=check_upload_file(form)
      post.description = form.description.data
      post.image = db_file_path
      post.ticket_num = form.ticket_num.data
      post.ticket_price = form.ticket_price.data
      post.event_date = form.event_date.data
      post.starting_date = form.starting_date.data
      post.closing_date = form.closing_date.data
      post.Event_status = form.Event_status.data
      # Update Database
      db.session.add(post) 
      db.session.commit()
      flash("Post Has Been Updated.")
      return redirect(url_for('destination.show', id=post.id))
    form.name.data = post.name
    form.description.data = post.description
    form.image.data = post.image
    form.ticket_num.data = post.ticket_num
    form.ticket_price.data = post.ticket_price
    form.event_date.data = post.event_date
    form.starting_date.data = post.starting_date
    form.closing_date.data = post.closing_date
    form.Event_status.data = post.Event_status
    return render_template('edit_event.html', form=form)
  
  else:
    return jsonify(message='To edit this event, you must be the creator of it.'), 200
  
  
  
def to_dictionary(self):
  h_dict = {b.name: str(getattr(self, b.name)) for b in self.destinations.columns}
  return h_dict