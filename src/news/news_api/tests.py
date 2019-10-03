from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

# initialize the APIClient app
client = Client()

# Create your tests here.
class GetAllNewsTest(TestCase):
    """ Test module for listing news API """

    def test_get_all_news(self):
        # get API response
        response = client.get('/api/news/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)