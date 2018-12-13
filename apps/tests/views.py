import logging
import smtplib
import time
from email.message import EmailMessage

import requests
from django.shortcuts import render
# Create your views here.
from rest_framework import status, views
from rest_framework.response import Response

from apps.auth_jwt.permissions import PublicEndpoint
from apps.tests.models import Test
from backend import settings

logger = logging.getLogger(__name__)

class TestDRFView(views.APIView):
    """

    """
    permission_classes = (PublicEndpoint,)

    def get(self, request):
        logger.info("Delay for 10 seconds")



        # time.sleep(10)
        # count = 1
        # while (count < 999):
        #     print('The count is:', count)
        #     count = count + 1
        return Response(['ok'])


class TestDRFDataBaseView(views.APIView):
    """

    """
    permission_classes = (PublicEndpoint,)

    def get(self, request):
        logger.debug("Delete all Test objects from database")
        try:
            Test.objects.all().delete()
        except Exception as ex:
            logger.error(str(ex))
            return Response(['error %s' % str(ex)], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        count = 1

        while (count < 100):
            str_count = str(count)
            Test(text=str_count).save()
            count = count + 1

        count = len(Test.objects.all())

        return Response(['ok'])


class TestDRFESView(views.APIView):
    """

    """
    permission_classes = (PublicEndpoint,)

    def get(self, request):
        try:
            es_search = requests.get(settings.ELASTIC_SEARCH_URL + "/_aliases")
            alias_list_json = es_search.json()
        except Exception as e:
            logger.error("Error getting aliases from Elastic Search %s" % e)
            return Response('app_elastic error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(alias_list_json)
