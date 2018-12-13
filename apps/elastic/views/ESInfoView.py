import requests
from rest_framework import status, views
from rest_framework.response import Response

from apps.auth_jwt.permissions import PublicEndpoint
from apps.log.mixins import RequestLogViewMixin
from backend import settings


class ESInfoView(RequestLogViewMixin, views.APIView):
    """

    """
    permission_classes = (PublicEndpoint,)

    def get(self, request):
        es_info = {}

        try:
            es_response = requests.get(settings.ELASTIC_SEARCH_URL + "/_cluster/health?format=json&pretty")
            es_info['cluster'] = es_response.json()
        except Exception as e:
            return Response('app_elastic error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            es_response = requests.get(settings.ELASTIC_SEARCH_URL + "/_cat/count?format=json&pretty")
            es_info['count'] = es_response.json()
        except Exception as e:
            return Response('app_elastic error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            es_response = requests.get(settings.ELASTIC_SEARCH_URL + "/_cat/indices?format=json&pretty")
            es_info['indices'] = es_response.json()
        except Exception as e:
            return Response('app_elastic error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            es_response = requests.get(settings.ELASTIC_SEARCH_URL + "/_aliases?format=json&pretty")
            es_info['aliases'] = es_response.json()
        except Exception as e:
            return Response('app_elastic error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(es_info, status=status.HTTP_200_OK)
