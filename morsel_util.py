import json
from crypt import crypt
from time import time
from time import sleep
from os.path import exists
from os import unlink
from hashlib import md5

def waitForLock(lock):
  delay = 0.1
  while exists("."+lock):
    delay += 0.1
    if (delay == 3):
      unlink("."+lock)
    sleep(0.1)

def getUsers():
  with open("users.json", "r") as users:
    json_bits = json.load(users)
    users.close()
  return json_bits

def getBoards():
  with open("boards.json", "r") as boards:
    json_bits = json.load(boards)
    boards.close()
  return json_bits

def passchk(name, pwd):
  for i in getUsers()["users"]:
    if i["name"] == name:
      print("Found user:",name)
      if crypt(pwd, str(int(time()))) == i["token"]:
        print("Password matches!")
        return True
      else:
        print("Password does not match.")
        return False
  return None

def tokenchk(name, token):
  for i in getUsers()["users"]:
    if i["name"] == name:
      if token == i["token"]:
        return True
      else:
        print(token)
        print(i["token"])
        return False
  return None

def uexist(name):
  for i in getUsers()["users"]:
    if i["name"] == name:
      return True
  return False

def getUser(name):
  users = getUsers()["users"]
  for user in users:
    if user["name"] == name: return user
  return None

def getUserPos(name):
  try:
    users = getUsers()["users"]
    i = 0
    for user in users:
      if user["name"] == name: return i
      i += 1
  except:
    return None

def bexist(name):
  for i in getBoards()["boards"]:
    if i["name"] == name:
      return i
  return False

def newuser(name, password):
  pwd = crypt(password, str(int(time())))
  users = getUsers()
  users["users"].append({
    "name": name,
    "token": pwd,
    "credate": int(time()),
    "grv_email": None,
    "subscriptions": []
  })
  with open("users.json", "w") as users_file:
    users_file.write(json.dumps(users, indent=2))
    users_file.close()
  return True

def newboard(name, mod):
  boards = getBoards()
  for i in boards["boards"]:
    if i["name"] == name:
      return False
  boards["boards"].append({
    "name": name,
    "founder": mod,
    "description": "A board on Morsel!",
    "moderators": [mod],
    "credate": int(time()),
    "posts": f"boards/{name}.json"
  })
  with open("boards.json", "w") as boards_file:
    boards_file.write(json.dumps(boards, indent=2))
    boards_file.close()
  with open(f"boards/{name}.json", "x") as file:
    file.write(json.dumps({
      "posts": {
        0: {
          "author": mod,
          "credate": int(time()),
          "content": f"Hello, {name}!"
        }
      }
    }, indent=2))
    file.close()
  return True

def subscribe(user, board):
  if bexist(board) and uexist(user):
    users=getUsers()
    users["users"][getUserPos(user)]["subscriptions"].append(board)
    with open("users.json", "w") as users_file:
      users_file.write(json.dumps(users, indent=2))
      users_file.close()
    return True
  return None

def unsubscribe(user, board):
  if bexist(board) and uexist(user) and is_subbed(user, board):
    users=getUsers()
    users["users"][getUserPos(user)]["subscriptions"].remove(board)
    with open("users.json", "w") as users_file:
      users_file.write(json.dumps(users, indent=2))
      users_file.close()
    return True
  return None

def is_subbed(user, board):
  if bexist(board) and uexist(user):
    user = getUser(user)
    subs = user["subscriptions"]
    for i in subs:
      if i == board:
        return True
    return False
  else: print("Lmao no")
  return None

def add_post(user, board, content):
  if bexist(board) and uexist(user) and len(content) < 1000:
    b = getBoards()["boards"]
    for candidate in b:
      print(candidate["name"], board)
      if candidate["name"] == board:
        posts = {}
        with open(candidate["posts"], "r") as posts_file:
          posts = json.loads(posts_file.read())
          posts_file.close()
        # this gets the new post ID
        postid = len(posts["posts"])
        posts["posts"][str(postid)] = {
          "author": user,
          "credate": int(time()),
          "content": content
        }
        with open(candidate["posts"], "w") as posts_file:
          posts_file.write(json.dumps(posts, indent=2))
          posts_file.close() 
        return True
    print("nope")

def libravatar_geturl(user):
  if uexist(user):
    u = getUser(user)
    if u["lrv_email"] == None:
      return "/static/default_avatar.png"
    else:
      hash = md5(u["lrv_email"].encode()).hexdigest()
      return f"https://seccdn.libravatar.org/avatar/{hash}?s=64"

def getRecentPosts(board, count):
  if bexist(board):
    posts = {}
    b = getBoards()["boards"]
    for candidate in b:
      print(candidate["name"], board)
      if candidate["name"] == board:
        with open(candidate["posts"], "r") as posts_file:
          posts = json.loads(posts_file.read())["posts"]
          posts_file.close()
    if posts == {}:
      return False
    else:
      array_posts = []
      array_count = 0

      for post in posts:
        tmp_post = posts[post]
        tmp_post["author_avatar"] = libravatar_geturl(tmp_post["author"])
        array_posts.append(tmp_post)
      array_posts = array_posts[::-1]
      
      if len(array_posts) > 20: return array_posts[:20]
      else: return array_posts
