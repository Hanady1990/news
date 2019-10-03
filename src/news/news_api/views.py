from rest_framework import viewsets, exceptions
from django.shortcuts import render
from rest_framework.response import Response

from newsapi import NewsApiClient
from collections import namedtuple
from datetime import datetime, timedelta

import json
import requests
import sys
import praw
import logging

from news import settings


class NewsViewSet(viewsets.GenericViewSet):

	def list(self, request):
		try:

			# News API
			today = datetime.today().date()
			news_api_url = '{0}?q=bitcoin&from={1}&sortBy=publishedAt&apiKey={2}'.format(settings.NEWS_API_URL, today, settings.NEWS_API_KEY)
			response = requests.get(url=news_api_url, headers={'content-type': 'application/x-www-form-urlencoded'})
			json_object = response.json()

			articles = json_object['articles']

			resp_obj = [] #final array
			
			# Append News API data
			for article in articles:
				json_article = {'headline': article['title'], 'link': article['url'], 'source': 'newsapi'}
				resp_obj.append(json_article)


			# Reddit
			reddit_api_url = '{0}'.format(settings.REDDIT_API_URL)
			response = requests.get(url=reddit_api_url, headers={'content-type': 'application/x-www-form-urlencoded'})
			json_object = response.json()
			
			articles = json_object['data']['children']

			
			# Append Reddit API data
			for article in articles:
				json_article = {'headline': article['data']['title'], 'link': article['data']['url'], 'source': 'reddit'}
				resp_obj.append(json_article)



			return Response(resp_obj)


		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments:\n{1!r} ---  line {2}"
			message = template.format(type(ex).__name__, ex.args, sys.exc_info()[-1].tb_lineno)
			log_error(message, 'NewsViewSet/list')
			raise exceptions.APIException(message)

def log_error(message, endpoint):
	error_logger = logging.getLogger('error_logger')
	error_logger.error('{} in {} at: {}'.format(message, endpoint, str(datetime.now())))

def log_info(message, endpoint):
	info_logger = logging.getLogger('info_logger')
	info_logger.info('{} in {} at: {}'.format(message, endpoint, str(datetime.now())))

