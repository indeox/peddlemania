__author__ = "tom@leitchy.com (Tom Leitch)"

import logging
import time
import datetime

from google.appengine.ext import db
from google.appengine.api import datastore_types
from google.appengine.ext import search

import sys ##getdefaultencoding()
import pprint
import string

	

class User(db.Model):
  user_id = db.StringProperty()
  name = db.TextProperty()
  user_timeline = db.StringProperty()
  image = db.StringProperty()
  lang = db.StringProperty()
  
  

class UsersOnPhone(db.Model):
	uuid = db.StringProperty()
	user = db.ReferenceProperty(User)
	oauth_id = db.StringProperty(required=False)

class HiScore(db.Model):
  user_id = db.ReferenceProperty(User)
  score = db.IntegerProperty(default=0)
  last_score = db.DateTimeProperty(auto_now_add=False)


class OAuthAccessToken(db.Model):
	"""OAuth Access Token."""

	user_id = db.StringProperty()
	user = db.ReferenceProperty(User)
	oauth_token = db.StringProperty()
	oauth_token_secret = db.StringProperty()
	created = db.DateTimeProperty(auto_now_add=True)
	

