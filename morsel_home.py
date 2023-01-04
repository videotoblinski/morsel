from flask import request
from flask import render_template
from main import app
from morsel_util import *

@app.route('/', methods=['POST', 'GET'])
def homepage():
  uname = request.cookies.get('username')
  token = request.cookies.get('token')
  loggedin = tokenchk(uname, token)
  if loggedin == True:
    return render_template('home.html', name=uname)
  elif loggedin == False:
    return render_template('loggedout.html')
  elif loggedin == None:
    return render_template('landing.html')
