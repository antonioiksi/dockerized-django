import requests
from rest_framework import status, views
from rest_framework.response import Response

from apps.auth_jwt.permissions import PublicEndpoint
from apps.log.mixins import RequestLogViewMixin
from backend import settings


class MappedFieldListView(RequestLogViewMixin, views.APIView):
    """

    """
    permission_classes = (PublicEndpoint,)

    def get(self, request):
        alias_list = [];

        try:
            es_search = requests.get(settings.ELASTIC_SEARCH_URL + "/_mapping")
            response_mapping = es_search.json()

            # output_dict = [x for x in data if x['type'] == '1']
            #values_arr = [x['_source']['play_name'] for x in data['hits']['hits']]
            #pprint(values_arr)
        except Exception as e:
            return Response('app_elastic error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        attributes = {}

        for index_name, index_mapping in response_mapping.items():
            tables_res = {}
            for table_name in index_mapping['mappings']:
                table_mapping = index_mapping['mappings'][table_name]
                if 'properties' in table_mapping:
                    temp_dict = table_mapping['properties']
                    #fields_arr = [temp_dict[key] for key in temp_dict if temp_dict[key].get('fields') is not None]
                    fields_arr = [temp_dict[key].get('fields') for key in temp_dict if temp_dict[key].get('fields') is not None]

                    for field in fields_arr:
                        for k in field.keys():
                            attributes[k]=''

                    #tables_res[table_name] = field_arr
                    #attributes.append(field_arr)

            #mappings_res[index_name] = tables_res

        return Response(attributes)
