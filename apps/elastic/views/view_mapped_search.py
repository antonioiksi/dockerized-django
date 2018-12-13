import json

import requests
from rest_framework import status, views
from rest_framework.response import Response

from apps.auth_jwt.permissions import PublicEndpoint
from apps.log.mixins import RequestLogViewMixin
from backend import settings


class MappedSearchView(RequestLogViewMixin, views.APIView):
    """
    Make search according official ElasticSearch docs.
    In fact it transports json to ES and return result filtering by 'hits' node in json
    request.data:
    json request must comply with ElasticSearch rules (https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
    """
    permission_classes = (PublicEndpoint,)

    def post(self, request, *args, **kwargs):
        #serializer = QuerySerializer(data=request.data)
        #serializer.is_valid()
        #js = serializer.validated_data
        # TODO add checking input param http://json-schema.org/

        # request.data
        # raise Exception("asdasdasdasd");

        r = requests.post(settings.ELASTIC_SEARCH_URL+"/_search?size="+settings.ELASTIC_SEARCH_RESULT_NUMBER,
                          json.dumps(request.data))
        search = r.json()

        mappings_res = {}
        hits_arr = search['hits']['hits']
        for hit in hits_arr:
            index_name = hit['_index']
            if index_name not in mappings_res:
                try:
                    es_mapping = requests.get(settings.ELASTIC_SEARCH_URL + '/' + index_name + '/_mapping')
                    mapping = es_mapping.json()
                except Exception as e:
                    return Response('app_elastic error getting mapping: %s' % e,
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                mapping = mapping[index_name]['mappings']

                tables_res = {}
                for table_name in mapping:
                    table_mapping = mapping[table_name]
                    # d = mapping[index_name]['mappings']['act']['properties']
                    # tables_mapping = [mapping[key] for key in mapping]
                    temp_dict = table_mapping['properties']

                    field_arr = {key: temp_dict[key] for key in temp_dict if temp_dict[key].get('fields') is not None}

                    tables_res[table_name] = field_arr

                mappings_res[index_name] = tables_res

        #count = 1
        #while (count < 999):
        #    print('The count is:', count)
        #    count = count + 1

        if r.status_code == 200:
            result = {}
            result['data'] = search['hits']['hits']
            result['mapping'] = mappings_res

            return Response( result, status=status.HTTP_200_OK)
        else:
            return Response('app_elastic error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
