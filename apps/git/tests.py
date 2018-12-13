from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, RequestsClient

from apps.git.views import GitVersionView


class GitTest(TestCase):
    """ Test module """

    def setUp(self):
        User.objects.create(username='admin')
        # user = User.objects.get(username='antonio')

    def test_GitVersionView(self):
        factory = APIRequestFactory()
        view = GitVersionView.as_view()
        url = '/git/version/'
        request = factory.get(url)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
