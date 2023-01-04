from main import app
from morsel_util import *

@app.route("/post/<board>")
def editor(board):
  if bexist(board):
    boards = getBoards()["boards"]
    for i in boards:
      if i["name"] == board:
        if "exp" in i:
          if i["exp"]:
            return "Cool"
          else:
            return "Not Cool"
        else: return "Not Cool"
    return "Bad"
  else:
    return "Bad"
