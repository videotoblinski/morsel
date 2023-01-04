from flask import request
from flask import render_template
from flask import redirect
from main import app
from morsel_util import *

def session_start(form):
  resp = redirect("/", code=303)
  resp.set_cookie('username', form['username'])
  resp.set_cookie('token', crypt(form['password'], str(int(time()))))
  return resp

@app.route('/login', methods=['POST', 'GET'])
def login():
  error = None
  if request.method == 'POST':
    if passchk(request.form['username'], request.form['password']):
      return session_start(request.form)
    else:
      error = 'Invalid username/password'

  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  resp = redirect("/", code=303)
  resp.delete_cookie('username')
  resp.delete_cookie('token')
  return resp

@app.route('/reg', methods=['POST', 'GET'])
def register():
  error = None
  if request.method == 'POST':
    if (not uexist(request.form['username'])) and len(request.form['password']) >= 8:
      newuser(request.form['username'], request.form['password'])
    elif len(request.form['password']) < 8:
      error = "Password must be at least 8 characters."
    else:
      error = "Username already taken."

  return render_template('register.html', error=error)
