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


class MainHandler(webapp.RequestHandler):
	def get(self):
		self.response.out.write('Hello world!')


class AuthoriseUserCompleteHandler(ViewController):
	def get(self):
		pass

class HiScoreHandler(ViewController):
	pass
	
class UserHandler(ViewController):
	pass


class NewUserHandler(ViewController):
	def post(self):
		pass


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
		logging.info(result.content)
		return self.response.out.write(user_info)
		


def main():

	application = webapp.WSGIApplication([
										('/', MainHandler),
										('/oauth/complete', CompleteAuthorisationHandler),

										('/hiscores', HiScoreHandler),
										('/u/(.*)', UserHandler),
										('/u/new', NewUserHandler), 
										('/us/authorise', AuthoriseUserHandler),
										('/u/authorise/complete', AuthoriseUserCompleteHandler),
										
										],
										 debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
