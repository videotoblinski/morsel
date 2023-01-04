from flask import request
from flask import render_template
from flask import redirect
from main import app
from morsel_util import *

@app.route('/b')
@app.route('/b/')
def boards():
  uname = request.cookies.get('username')
  token = request.cookies.get('token')
  loggedin = tokenchk(uname, token)
  if loggedin == True:
    boards = getBoards()
    subbed = getSubbedArray(uname, boards)
    return render_template('boards.html', name=uname, boards=boards["boards"], subbed=subbed)
  elif loggedin == None:
    return render_template('landing.html')

@app.route('/postto/<board>', methods=['POST'])
def createpost(board):
  uname = request.cookies.get('username')
  token = request.cookies.get('token')
  loggedin = tokenchk(uname, token)
  if loggedin == True:
    add_post(uname, board, request.form["postbody"])
    return redirect(request.referrer, 303)

@app.route('/subs')
@app.route('/subs/')
def subs():
  uname = request.cookies.get('username')
  token = request.cookies.get('token')
  loggedin = tokenchk(uname, token)
  if loggedin == True:
    boards = getBoards()
    print(boards)
    subbed = getSubbedArray(uname, boards)
    if len(subbed) != 0:
      subboards = []
      for board in boards["boards"]:
        if board["name"] in subbed:
          subboards.append(board)
      return render_template('boards.html', name=uname, boards=subboards, subbed=subbed)
    else:
      return render_template('err.html', err="You are not subscribed to any boards.", refer="/b/")
  elif loggedin == None:
    return render_template('landing.html')

def getSubbedArray(user, boards):
  subbed = []
  for i in boards["boards"]:
    if is_subbed(user, i["name"]):
      subbed.append(i["name"])
  return subbed

@app.route('/b/<board>')
def viewboard(board):
  uname = request.cookies.get('username')
  token = request.cookies.get('token')
  loggedin = tokenchk(uname, token)
  if loggedin == True:
    boardget = bexist(board)
    if boardget == False:
      return render_template('noboard.html', name=uname, board=board)
    else:
      args = request.args.to_dict()
      if "subscribe" in args:
        subscribe(uname, boardget["name"])
        return redirect(request.referrer, 303)
      elif "unsubscribe" in args:
        unsubscribe(uname, boardget["name"])
        return redirect(request.referrer, 303)
      return render_template(
        'board.html', name=uname,
         bname=boardget["name"],
         bdesc=boardget["description"],
         bmods=", ".join(boardget["moderators"]),
         subbed=is_subbed(uname, board),
         posts=getRecentPosts(board, 20),
         uavatar=libravatar_geturl(uname)
      )
  elif loggedin == None:
    return render_template('landing.html')
