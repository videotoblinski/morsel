from flask import Flask
from flask import render_template
from flask import request
from flask import url_for

app = Flask(__name__)

import morsel_home
import morsel_login
import morsel_boards
import morsel_post
