from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate


class LogTest(TestCase):
    """ Test module for Log model """

    def setUp(self):
        User.objects.create(username='antonio')
        user = User.objects.get(username='antonio')

    def test_log(self):
        user = User.objects.get(username='antonio')

        self.assertEqual(1, 1)

    def test_UserBinLogViewSet(self):

        self.assertEquals
