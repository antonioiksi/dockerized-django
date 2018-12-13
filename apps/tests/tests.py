from django.test import TestCase
# Create your tests here.
from rest_framework import status
from rest_framework.test import APIRequestFactory

from apps.tests.views import TestDRFView


class TestsTest(TestCase):

    def test_TestDRFView(self):
        factory = APIRequestFactory()
        req = factory.get('/tests/drf')
        #force_authenticate(req, user=user)
        view = TestDRFView.as_view()
        resp = view(req)
        self.assertEqual( resp.status_code, status.HTTP_200_OK)


    def test_TestESviaDRFView(self):
        factory = APIRequestFactory()
        req = factory.get('/tests/es-via-drf')
        #force_authenticate(req, user=user)
        view = TestDRFView.as_view()
        resp = view(req)
        self.assertEqual( resp.status_code, status.HTTP_200_OK)
