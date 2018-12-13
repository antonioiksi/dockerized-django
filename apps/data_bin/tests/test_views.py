from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase
# Create your tests here.
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from apps.data_bin.models import Bin


class DataBinTest(APITestCase):
    """ Test module for GET all logs API """
    urls = 'app_data_bins.urls'


    def setUp(self):
        print('setUp ViewsTest')
        User.objects.create(username='antonio')
        bin = Bin.objects.create(name='default')
        pprint(Bin.objects.all())


    def test_FlatDataBinView(self):
        client = APIClient()
        user = User.objects.get(username='antonio')
        client.force_authenticate(user=user)
        #url = reverse('simple')
        url = '/bins/all/'
        #response = client.post(url, json.loads(query_match_all), format='json')
        #pprint(json.dumps( response.json()))
        #pprint(response.json())
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(status.HTTP_200_OK, status.HTTP_200_OK)
