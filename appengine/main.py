#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import models
import logging

import simplejson
import urllib
import urllib2
from django.utils import simplejson

from viewcontroller import ViewController

from challengehandlers import ChallengeSelectHandler, ChallengeHandler, ChallengeCompleteHandler
from userhandlers import CompleteAuthorisationHandler, NewUserHandler, AuthoriseUserHandler, AuthoriseUserCompleteHandler, UserHandler, NewUserHandler


class MainHandler(ViewController):
	def get(self):
	
		#if (self.isAuthenticated()):
		return self.output('home')
		#else:
		#	return self.redirect('/u/new')
	def post(self):
		self.get()


class HiScoreHandler(ViewController):
	def get(self):
		pass	
	def post(self):
		self.get()
	

class PopulateHandler(ViewController):

	def get(self):
	
		url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20xml%20where%20url%3D'http://api.bike-stats.co.uk/service/rest/bikestats'&format=json&diagnostics=true"

		
		page = urllib2.urlopen(url)
		if page:
			data = page.read()
			result = simplejson.loads(data)
			if result['query'] is None:
				return
			if result['query']['results'] is None:
				return
				
			for station in result['query']['results']['dockStationList']['dockStation']:
				name = station['name'].replace('\n', '').lstrip("\s")
				id = models.Place.generate_key(station['ID'])
				place = models.Place.get_or_insert(key_name=id, name=name, lat=float(station['latitude']), long=float(station['longitude']))
				#place = models.Place.create(station['ID'], name=name, lat=float(station['latitude']), long=float(station['longitude']))
				place.put()
				
				#logging.info(models.Place.get(station['ID']))
				#logging.info(models.Place.get_by_key_name()))
		

def main():

	application = webapp.WSGIApplication([
										('/', MainHandler),
										('/oauth/complete', CompleteAuthorisationHandler),

										('/u/new', NewUserHandler), 
										('/u/authorise', AuthoriseUserHandler),
										('/u/authorise/complete', AuthoriseUserCompleteHandler),
										('/u/(.*)', UserHandler),
										('/u/new', NewUserHandler), 
										
										## all about the challenges.
										('/challenge',  ChallengeSelectHandler), 
										
										('/challenge/start',  ChallengeHandler), 
										('/challenge/complete',  ChallengeCompleteHandler), 
										
										
										
										('/hiscores', HiScoreHandler),
										
										('/task/populate', PopulateHandler),
										],
										 debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
