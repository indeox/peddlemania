#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import cgi
import time
from datetime import tzinfo, timedelta, datetime, date

import re
import warnings
import logging
from pprint import pprint

from viewcontroller import ViewController
import models

import oauth


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

class AuthoriseUserCompleteHandler(ViewController):
	def get(self):
	
		oauth_token = self.request.cookies.get('oauth_token')
		
		if oauth_token is None:
			raise Exception("No Twitter access token")
			
		token = models.OAuthAccessToken.get_by_key_name(oauth_token)
		if oauth_token is None:
			raise Exception("No Twitter access - could not verify token")
		
		
		#user = models.User.get_by_key_name(token.user_id)
		#return self.output('user/authorise_complete', {'user': user, 'token': token})
		self.redirect('/')
	def post(self):
		return self.get()


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