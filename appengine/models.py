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
	image = db.StringProperty()
  	total_score = db.IntegerProperty(default=0)
  	journeys = db.ListProperty(db.Key)
 

class Place(db.Model):
	name = db.StringProperty()
	lat = db.FloatProperty()
	long = db.FloatProperty()
	
	@classmethod
	def generate_key(cls, id):
		return "place_%s" % (id)
		
  	@classmethod
	def get(cls, id):
		key = cls.generate_key(id)
		return cls.get_by_key_name(key)
		
  	@classmethod
	def create(cls, id, **kwargs):
		key = cls.generate_key(id)
		logging.info(kwargs)
		return cls.get_or_insert(key_name=id, **kwargs)
		
	
class Journey(db.Model):
	from_id = db.IntegerProperty()
	to_id = db.IntegerProperty()
	from_place = db.ReferenceProperty(Place, collection_name='from')
	to_place = db.ReferenceProperty(Place, collection_name='to')
	distance = db.FloatProperty()
	fastest_user = db.ReferenceProperty(User, collection_name='fastest_time')
	num_of_journeys = db.IntegerProperty(default=0)
	highest_scoring_user = db.ReferenceProperty(User, collection_name='highest_score')
	
	@classmethod
	def generate_key(cls, from_id, to_id):
		return "journey_%s_%s" % (from_id, to_id)
	
  	@classmethod
	def get(cls, from_id, to_id):
		key = cls.generate_key(from_id, to_id)
		return cls.get_by_key_name(key)


class UserJourney(db.Model):
 	journey = db.ReferenceProperty(Journey)
 	user = db.ReferenceProperty(User)
 	date = db.DateTimeProperty(auto_now_add=True)
 	completed_time = db.IntegerProperty()
 	fullness_score = db.IntegerProperty(default=0)
 	incomplete = db.BooleanProperty(default=True)
 	score = db.IntegerProperty(default=0)
 	

	
class HighScores(db.Model):
	#journey = db.ReferenceProperty()
	pass


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
	

