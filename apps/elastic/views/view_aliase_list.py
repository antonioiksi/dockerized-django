import requests
from rest_framework import status, views
from rest_framework.response import Response

from apps.auth_jwt.permissions import PublicEndpoint
from apps.log.mixins import RequestLogViewMixin
from backend import settings


class AliasListView(RequestLogViewMixin, views.APIView):
    """

    """
    permission_classes = (PublicEndpoint,)

    def get(self, request):
        alias_list = [];

        try:
            es_search = requests.get(settings.ELASTIC_SEARCH_URL + "/_aliases")
            alias_list_json = es_search.json()

            # output_dict = [x for x in data if x['type'] == '1']
            #values_arr = [x['_source']['play_name'] for x in data['hits']['hits']]
            #pprint(values_arr)
        except Exception as e:
            return Response('app_elastic error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(alias_list_json)
