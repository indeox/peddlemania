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


import oauth

import models
import logging
from datetime import tzinfo, timedelta, datetime, date

from viewcontroller import ViewController

OAUTH_APP_SETTINGS = {

    'twitter': {

        'consumer_key': '13t994ZKfhhmdmFQbsNeg',
        'consumer_secret': 'I7i1nTU0ckUb74AXpIXiIy305GV4BOXzqobh4gsfNqQ',

        'request_token_url': 'https://twitter.com/oauth/request_token',
        'access_token_url': 'https://twitter.com/oauth/access_token',
        'user_auth_url': 'http://twitter.com/oauth/authorize',

        'default_api_prefix': 'http://twitter.com',
        'default_api_suffix': '.json',

        }
    }


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

class AuthoriseUserCompleteHandler(ViewController):
	def get(self):
	
		oauth_token = self.request.cookies.get('oauth_token')
		
		if oauth_token is None:
			raise Exception("No Twitter access token")
			
		token = models.OAuthAccessToken.get_by_key_name(oauth_token)
		if oauth_token is None:
			raise Exception("No Twitter access - could not verify token")
		
		
		user = models.User.get_by_key_name(token.user_id)
	
		return self.output('user/authorise_complete', {'user': user, 'token': token})
	def post(self):
		return self.get()

class HiScoreHandler(ViewController):
	pass
	
class UserHandler(ViewController):
	pass



class NewUserHandler(ViewController):
	def post(self):
		return self.get()
	def get(self):
		return self.output('user/new')


class AuthoriseUserHandler(ViewController):
	def get(self):
		callback_url = "%s/oauth/complete" % self.request.host_url
    
		client = oauth.TwitterClient(OAUTH_APP_SETTINGS['twitter']['consumer_key'], OAUTH_APP_SETTINGS['twitter']['consumer_secret'], callback_url)
		return self.redirect(client.get_authorization_url())


class CompleteAuthorisationHandler(ViewController):
	def get(self):
		callback_url = "%s/oauth/complete" % self.request.host_url
		client = oauth.TwitterClient(OAUTH_APP_SETTINGS['twitter']['consumer_key'], OAUTH_APP_SETTINGS['twitter']['consumer_secret'], callback_url)
		
		auth_token = self.request.get("oauth_token")
		auth_verifier = self.request.get("oauth_verifier")
		user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)

		
		timeline_url = "http://twitter.com/statuses/user_timeline.xml"
		result = client.make_request(url=timeline_url, token=auth_token, secret=auth_verifier)

		if user_info['username'] is None:
			raise Exception("no username")
			
		user_timeline = "twitter.com/statuses/user_timeline/%s.rss" % user_info['id']
		
		user = models.User.get_or_insert(key_name=user_info['username'], 
													name=user_info['name'], 
													user_id=user_info['username'],
													user_timeline=user_timeline, 
													image=user_info['picture'],
													lang='en')
		
		if user is None:
			raise Exception("No user created")
		
		
		oauth_token = models.OAuthAccessToken.get_or_insert(key_name=user_info['token'], 
																user_id=user_info['username'],
																oauth_token=user_info['token'], 
																oauth_token_secret=user_info['secret'])

		self.redirect('/u/authorise/complete')
		self.response.headers.add_header('Set-Cookie', ('oauth_token=%s; expires=Sun, 12-December-2050 23:59:59 GMT; path=/;' % user_info['token'])) 
		
		
		return
		


##### challenge handlers....

class ChallengeSelectHandler(ViewController):
	def get(self):
		
		pass
	def post(self):
		self.get()



class ChallengeCompleteHandler(ViewController):
	def get(self):
		self.post()  #make sure to change this.
	def post(self):
		from_id = self.request.get("from_id")
		to_id = self.request.get("to_id")
		score = self.request.get("score")
		user_details = self.getUserDetails()
		
		
		if user_details is None:
			return self.error('No user found')
		
		if score is None or score == '':
			return self.error('Unable to calculate score')
		else:
			score = int(score)
		
		journey = models.Journey.get(from_id, to_id)
		
		if journey is None:
			return self.error('This journey was not found')
		
		q = models.UserJourney.gql("WHERE user = :1 AND journey = :2 AND incomplete = True", user_details, journey)
		user_journey = q.get()

		if user_journey is None:
			return self.error('Your journey was not found, or has been completed already')
			
		#user_journey.incomplete = False
		start_end_diff = datetime.now() - user_journey.date
		user_journey.completed_time = unicode(start_end_diff)
		user_journey.score = score
		user_journey.put()
		
		user_details.total_score += score
		user_details.put()
		
		
		fastest_user = False
		q = models.UserJourney.gql("WHERE user = :1 AND journey = :2", journey.fastest_user, journey)
		fastest_user_journey = q.get()
		if fastest_user_journey:
			fastest_time =  datetime.strptime(fastest_user_journey.completed_time, '%H:%M:%S.')
			logging.info(fastest_time)
			logging.info(fastest_time - start_end_diff)
			#if current_fastest < journey_time -- fastest_user = True
		else:
			journey.fastest_user = user_details
			fastest_user = True
			logging.info('Fastest user!')
		
		journey.num_of_journeys += 1
		journey.put()
		
		
		logging.info('finished')
		return self.output('challenge_complete', {'user_journey': user_journey, 'journey': journey, 'user': user_details})


class ChallengeHandler(ViewController):
	def get(self):
		
		return self.post() ## remove
	def post(self):
	
		from_id = self.request.get("from_id")
		to_id = self.request.get("to_id")
		distance = self.request.get("distance")
		fullness_score = self.request.get("fullness_score")
		user_details = self.getUserDetails()
		
		logging.info(user_details)
		
		if user_details is None:
			return self.error('No user found')
		
		journey = models.Journey.get(from_id, to_id)

		if distance is None or distance <= 0 or distance == '':
			return self.error('Distance must be a float')
			
		if (from_id is None or to_id is None) or (from_id == '' or to_id == ''):
			return self.error('Must provide From and To locations')
		
		if journey is None:
			j_key = models.Journey.generate_key(from_id, to_id)
			logging.info('Journey key: %s' % j_key)
			journey = models.Journey(key_name=j_key, distance=float(distance))
			journey.put()
		
		q = models.UserJourney.gql("WHERE user = :1 AND journey = :2", user_details, journey)
		user_journey = q.get()

		if user_journey is None:
			user_journey = models.UserJourney(user=user_details, journey=journey, fullness_score=fullness_score)
			user_journey.put()
		
		user_details.journeys.append(user_journey)
		user_details.put()
			
		return self.output('challenge', {'user_journey': user_journey, 'journey': journey, 'user': user_details})
		
		



def main():

	application = webapp.WSGIApplication([
										('/', MainHandler),
										('/oauth/complete', CompleteAuthorisationHandler),

										('/hiscores', HiScoreHandler),
										('/u/new', NewUserHandler), 
										('/u/authorise', AuthoriseUserHandler),
										('/u/authorise/complete', AuthoriseUserCompleteHandler),
										('/u/(.*)', UserHandler),
										
										
										## all about the challenges.
										('/challenge',  ChallengeSelectHandler), 
										
										('/challenge/start',  ChallengeHandler), 
										('/challenge/complete',  ChallengeCompleteHandler), 
										('/u/new', NewUserHandler), 
										],
										 debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
