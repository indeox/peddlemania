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
			
		start_end_diff = datetime.now() - user_journey.date	
		## convert journey time to seconds..
		m = re.match(r'(\d{1,3}):([0-5]\d):([0-5]\d)\.\d*$', str(start_end_diff))
		journey_seconds = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
			
			
		#user_journey.incomplete = False
		user_journey.completed_time = int(journey_seconds)
		user_journey.score = score
		user_journey.put()
		
		user_details.total_score += score
		user_details.put()
		
		
		### work out if this user journey is the fastest time of them all
		fastest_user = False
		q = models.UserJourney.gql("WHERE journey = :1 ORDER BY completed_time DESC", journey)
		fastest_user_journey = q.get()
		logging.info(fastest_user_journey.completed_time)
		if fastest_user_journey:
			if journey_seconds > fastest_user_journey.completed_time:
				fastest_user = True
				journey.fastest_user = user_details
		else:
			journey.fastest_user = user_details
			fastest_user = True
			
			
		#### work out if this user journey is the highest scoring of them all
		highest_scoring_user = False
		q = models.UserJourney.gql("WHERE journey = :1 ORDER BY score DESC", journey)
		highest_scoring_user_journey = q.get()
		if highest_scoring_user_journey:

			if score > highest_scoring_user_journey.score:
				highest_scoring_user = True
				journey.highest_score = user_details
		else:
			journey.highest_score = user_details
			highest_scoring_user = True
			
		
		journey.num_of_journeys += 1
		journey.put()
		
		
		logging.info('finished')
		return self.output('challenge_complete', {'user_journey': user_journey, 'journey': journey, 'user': user_details, 'fastest_user': fastest_user, 'highest_scoring_user': highest_scoring_user})


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
		
		if fullness_score is None or fullness_score <= 0 or fullness_score == '':
			fullness_score = 0

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
		
		user_details.journeys.append(user_journey.key())
		user_details.put()
			
		return self.output('challenge', {'user_journey': user_journey, 'journey': journey, 'user': user_details})