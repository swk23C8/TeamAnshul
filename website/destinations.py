from flask import Blueprint, render_template, request, redirect, url_for
from .models import Destination, Comment
from .forms import DestinationForm, CommentForm
from . import db, app
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user
from flask.json import jsonify

bp = Blueprint('destination', __name__, url_prefix='/destinations')

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
    ,poster_id=current_user)
        

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
  upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path='/static/image/' + secure_filename(filename)
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
  

  
  
  
  # Deleting the destination
@bp.route('/delete/<id>', methods = ['GET','DELETE'])
@login_required
def delete_show(id):
  id = current_user.id
  post_to_delete = Destination.query.get_or_404(id)
  if id == post_to_delete.poster.id:

    destination = Destination.query.filter_by(id=id).first()
    # create the comment form
    db.session.delete(destination)
    db.session.commit()
    return jsonify(message='deleted destination'), 200
    

  else:
      return jsonify(message='To delete this, you must be the creator of this Event.'), 200

      
      
  # Updating the destination
#@bp.route('/update/<id>', methods = ['GET', 'PUT'])
#@login_required
#def update_show(id):
#    json_dict = request.get_json()
#    destination = Destination.query.filter_by(id=id).first()
#    form = Updatedestination()
#    destination.name = json_dict['name']
#   if form.validate_on_submit():
#      destinations_updated = Destination.query.filter_by(id=id).update(
#        dict(name=(form.new_event_name.data),
#             name=(form.new_event_name.data)
#             ))
  
#    db.session.commit() 
#    return jsonify(message='Updated destination'), 200    
  
  
  #Converting into a JSON dict
#@bp.route('/update')
#@login_required
#def get_event(id):
#  events = Destination.query.all()
#  event_list = [D.to_dictionary() for D in events]
#  return jsonify(events=event_list) 
  
def to_dictionary(self):
  h_dict = {b.name: str(getattr(self, b.name)) for b in self.destinations.columns}
  return h_dict