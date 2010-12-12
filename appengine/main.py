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
	
		if (self.isAuthenticated()):
			
			user_details = self.getUserDetails()
			no_of_journeys = len(user_details.journeys)
			last_journey_key = user_details.journeys[-1]
			last_journey = models.UserJourney.gql("WHERE __key__ = :1", last_journey_key).get()
			logging.info(last_journey)
		
			return self.output('home', {
														'no_of_journeys': no_of_journeys,
														'user': user_details,
														'last_journey': last_journey,
													})
		else:
			return self.redirect('/u/new')
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



class UserHiScoreHandler(ViewController):
	def get(self):
		pass
	def post(self):
		pass
		
class PlaceHiScoreHandler(ViewController):
	def get(self, place_id):
		
		place = models.Place.get(place_id)
		
		if not place:
			return self.error('Unable to find that place')
			
		
		
	def post(self):
		pass
		
class HiScoreHandler(ViewController):
	def get(self):
		pass
	def post(self):
		pass


		

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
										
										## hi scores tables
										('/hiscores/by/user', UserHiScoreHandler),
										('/hiscores/by/place/(.*)', PlaceHiScoreHandler),
										('/hiscores/by/score', HiScoreHandler),
										
										('/task/populate', PopulateHandler),
										],
										 debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
