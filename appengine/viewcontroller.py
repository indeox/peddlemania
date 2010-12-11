#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import cgi
import time
import datetime
import os
import re
import sys
import warnings
import logging
import pprint
import simplejson

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import datastore_types

import models

from twitter_oauth_handler import OAuthClient

# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

class ViewController(webapp.RequestHandler):

	def __init__(self):
		self.client = None
		self.auth = False
		self.client_info = None
		self.client_rate_info = None
		self.user_db = None
		self.user_id = None

	def get(self, **kargs):
		pass
  
	def post(self, **kargs):
		pass
  
	def head(self, *args):
		pass
  
	def output(self, template_name, template_values={}, **kargs):
	
		values = {
			'request': self.request,
			'application_name': 'TweetMarkr',
		}
		values.update(template_values)
	
		output_format = self.request.get('format')

		if output_format:
			if output_format == 'json':
				suffix = '.json';
			elif output_format == 'xml':
				suffix = '.xml'
			else:
				suffix = '.html'
		else:
			suffix = '.html'

		template_path = template_name + suffix


		oauth_token = self.request.cookies.get('oauth_token')
		if oauth_token is not None:
			token = models.OAuthAccessToken.get_by_key_name(oauth_token)
			if token and token.oauth_token == oauth_token:
				values.update({ 'VERIFIEDUSER': self._getUserDetails(token.user_id) })
	
	
		output = ''
		if output_format == 'json':
			self.response.headers['Content-Type'] = 'text/json'
			output = simplejson.dumps(template_values, default=ViewController.to_dict)
		else:
			output = template.render('templates/' + template_path, values, debug=_DEBUG)
	  
		self.response.out.write(output)
		return



	def _getUserDetails(self, user_id):
		if not self.user_db:
			try:
	  			self.user_obj = models.User.get_by_key_name(user_id)
				return self.user_obj
			except Exception, e:
				logging.info(e)
				logging.info('Could not find user')
				return None
		else:
			return None


	def _checkAuthStatus(self):
		self.auth = False
		oauth_token = self.request.cookies.get('oauth_token')
		if oauth_token is not None:
			token = models.OAuthAccessToken.get_by_key_name(oauth_token)
    		if token is not None:
				self.auth = True
		
		return

	@staticmethod
	def to_dict(model, skipModels=False):
		output = {}
		SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)	  

		for key, prop in model.properties().iteritems():
			value = getattr(model, key)
			#logging.info(key)
			if value is None or isinstance(value, SIMPLE_TYPES):
				output[key] = unicode(value)
			elif isinstance(value, datetime):
				output[key] = str(value.strftime('%Y-%m-%d %H:%M%S %Z'))
			elif (isinstance(value, db.Model)):
				if (skipModels is False):
					output[key] = to_dict(value)
				else:
					output[key] = unicode(value.key().id_or_name())
			else:
				raise ValueError('cannot encode ' + repr(prop))
				
		return output