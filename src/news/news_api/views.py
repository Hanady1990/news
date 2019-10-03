from rest_framework import viewsets, exceptions
from django.shortcuts import render
from rest_framework.response import Response

from newsapi import NewsApiClient
from collections import namedtuple

import json
import requests
import praw

from news import settings


class NewsViewSet(viewsets.GenericViewSet):

	def list(self, request, pk=None):
		try:
			

			# Initialize News API client
			newsapi = NewsApiClient(api_key=settings.NEWS_API_KEY)

			url = 'https://newsapi.org/v2/everything?q=bitcoin&from=2019-09-04&sortBy=publishedAt&apiKey=927089e2072c4710840ca6d3fa9b7e50'
			response = requests.get(url=url, headers={'content-type': 'application/x-www-form-urlencoded'})
			json_object = response.json()

			articles = json_object['articles']
			resp_obj = []
			for article in articles:
				json_article = {'headline': article['title'], 'link': article['url'], 'source': 'News API'}
				resp_obj.append(json_article)

			return Response(resp_obj)
			x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
			return Response(x.source.id)

			
			# /v2/sources
			sources = newsapi.get_sources(category='general')
			myList = sources['sources']
			
			# url = 'https://newsapi.org/v2/everything?q=bitcoin&from=2019-09-01&sortBy=publishedAt&apiKey=927089e2072c4710840ca6d3fa9b7e50'

			# response = requests.get(url=url, headers={'content-type': 'application/x-www-form-urlencoded'})
			# json_object = response.json()

			# if json_object['status'] != 'ok':
			# 	raise exceptions.NotFound('Status is not OK')

			# return Response(json_object['articles'])

		except Exception as ex:
			template = "An exception of type {0} occurred. Arguments:\n{1!r}"
			message = template.format(type(ex).__name__, ex.args)
			raise exceptions.APIException(message)

