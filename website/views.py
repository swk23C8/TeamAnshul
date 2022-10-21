from flask import Blueprint, render_template, request, redirect,url_for
from .models import Destination 

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    destinations = Destination.query.all()    
    return render_template('index.html', destinations=destinations)

@mainbp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        dest = "%" + request.args['search'] + '%'
        
        dest1 = Destination.query.filter(Destination.description.like(dest)).all()
        
        dest2 = Destination.query.filter(Destination.name.like(dest)).all()
        
        destinations = dest1 + dest2
        return render_template('index.html', destinations=destinations)
    else:
        return redirect(url_for('main.index'))