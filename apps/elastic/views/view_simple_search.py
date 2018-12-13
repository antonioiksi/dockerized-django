import json

import requests
from rest_framework import status, views
from rest_framework.response import Response

from apps.log.mixins import RequestLogViewMixin
from backend import settings


class SimpleSearchView(RequestLogViewMixin, views.APIView):
    """
    Make search according official ElasticSearch docs.
    In fact it transports json to ES and return result filtering by 'hits' node in json
    request.data:
    json request must comply with ElasticSearch rules (https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
    """
    #permission_classes = (PublicEndpoint,)

    def post(self, request, *args, **kwargs):
        #serializer = QuerySerializer(data=request.data)
        #serializer.is_valid()
        #js = serializer.validated_data
        # TODO add checking input param http://json-schema.org/

        r = requests.post(settings.ELASTIC_SEARCH_URL+"/_search?size="+settings.ELASTIC_SEARCH_RESULT_NUMBER,
                          json.dumps(request.data))
        search = r.json()

        count = 1
        while (count < 999):
            print('The count is:', count)
            count = count + 1

        #source_arr = [x['_source'] for x in data['hits']['hits']]
        if r.status_code == 200:
            result = {}
            result['data'] = search['hits']['hits']

            return Response( result, status=status.HTTP_200_OK)
        else:
            return Response('app_elastic error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #raise APIException("There was a problem!")
