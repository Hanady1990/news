from rest_framework import viewsets, exceptions, status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from collections import namedtuple
from datetime import datetime, timedelta

import json
import requests
import sys
import logging

from news import settings


class NewsViewSet(viewsets.GenericViewSet):

	def list(self, request):
		"""
		An API that aggregates News API and Reddit data, and have the ability to search a keyword in the article.
		The returned response is a json array.
		Params:
		query (optional): string - keyword for search
		"""
		try:
			log_info("Listing all news.", "NewsViewSet/list")
			query = request.GET.get('query')
			log_info("Params: query={0}".format(query), "NewsViewSet/list")

			# News API
			news_api_url = '{0}?apiKey={1}&q={2}'.format(settings.NEWS_API_URL, settings.NEWS_API_KEY, query)
			response = requests.get(url=news_api_url, headers={'content-type': 'application/x-www-form-urlencoded'})
			json_object = response.json()
			#final array to be returned
			resp_obj = [] 

			# Check if response status is ok
			if response.status_code == status.HTTP_200_OK:
				articles = json_object['articles']

				# Append News API data
				log_info("Appending News API data.", "NewsViewSet/list")
				for article in articles:
					json_article = {'headline': article['title'], 'link': article['url'], 'source': 'newsapi'}
					resp_obj.append(json_article)
			else:
				log_error("Error retreiving News API data. Message: {0}, error code: {1}".format(json_object['message'], json_object['code']), "NewsViewSet/list")
				return Response(json_object['message'], status=response.status_code)


			# Reddit
			# Chech if search param is provided
			if query is not None and query != '':
				reddit_api_url = '{0}?q={1}&restrict_sr=1'.format(settings.REDDIT_SEARCH_API_URL, query)
			else:
				reddit_api_url = '{0}'.format(settings.REDDIT_API_URL)
			response = requests.get(url=reddit_api_url, headers={'content-type': 'application/x-www-form-urlencoded'})
			json_object = response.json()

			# Check if response status is ok
			if response.status_code == status.HTTP_200_OK:
				articles = json_object['data']['children']

				# Append Reddit API data
				log_info("Appending Reddit data.", "NewsViewSet/list")
				for article in articles:
					json_article = {'headline': article['data']['title'], 'link': article['data']['url'], 'source': 'reddit'}
					resp_obj.append(json_article)
			else:
				log_error("Error retreiving Reddit data. Message: {0}, error code: {1}".format(json_object['message'], json_object['error']), "NewsViewSet/list")
				return Response(json_object['message'], status=response.status_code)

			return Response(resp_obj)


		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments:\n{1!r}; line: {2}"
			message = template.format(type(ex).__name__, ex.args, sys.exc_info()[-1].tb_lineno)
			log_error(message, 'NewsViewSet/list')
			raise exceptions.APIException(message)

def log_error(message, endpoint):
	error_logger = logging.getLogger('error_logger')
	error_logger.error('{} in {} at: {}'.format(message, endpoint, str(datetime.now())))

def log_info(message, endpoint):
	info_logger = logging.getLogger('info_logger')
	info_logger.info('{} in {} at: {}'.format(message, endpoint, str(datetime.now())))

