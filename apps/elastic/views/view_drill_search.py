import json
import logging
from pprint import pprint

import requests
from rest_framework import status, views
from rest_framework.response import Response

from apps.attribute.models import MappingType
from apps.auth_jwt.permissions import PublicEndpoint
from apps.data_bin.utils import add_value, get_new_value
from apps.elastic.utils import prepare_q2
from apps.log.mixins import RequestLogViewMixin
from backend import settings
import time

from apps.elastic.utils import doubleQuoteDict

logger = logging.getLogger(__name__)

input_json = """
{

    "deep": "3",
    "style": "strong",
    [
        {
            "phone": "2345233425",
            "name": "name 1"
        },
        {
            "type": "234534534",
        }
    ]
}"""

input_query = """{'query': {'bool': {'should': [{'match': {'speaker': 'king'}},
                               {'match': {'play_name': 'Henry'}}]}}}"""

query_match_all = """
{
    "query": {
        "match_all": {}
    }
}"""




class DrillSearchView(RequestLogViewMixin, views.APIView):
    """



    """
    permission_classes = (PublicEndpoint,)

    def post(self, request, *args, **kwargs):
        # TODO add checking input param http://json-schema.org/

        # sif
        # body = json.loads(request.body.decode("utf-8"))
        jsonQuery = request.data['jsonQuery']

        try:
            mapping_type = MappingType.objects.filter(active=True)[0]
            endpoint = mapping_type.endpoint;
        except Exception as e:
            logger.error(str(e))
            return Response({'status': 'error', 'message': 'Не найден активный MappingType'}, status=status.HTTP_412_PRECONDITION_FAILED)

        es_url = endpoint + "/_search?size=" + settings.ELASTIC_SEARCH_RESULT_NUMBER


        try:
            es_query = prepare_q2(jsonQuery, mapping_type.id)

            headers = {'Content-type': 'application/json'}
            logger.info("requests.post url: " + es_url)
            logger.info(headers)
            logger.info(doubleQuoteDict(es_query))

            start = time.time()
            es_search = requests.post(es_url, data=json.dumps(es_query), headers=headers)
            # es_search = requests.post(es_url, data=json.dumps(es_query))
            # es_search = requests.get( es_url)
            end = time.time()
            logger.info("Request execution: " + str(end - start))

            search = es_search.json()
            try:
                hits_hits = search['hits']['hits']
            except:
                logger.error('Elastic return error')
                logger.error(search)
                return Response(
                            {'status': 'error',
                             'message': str(search),
                             'es_url': es_url,
                             'es_query': es_query},
                            status=status.HTTP_400_BAD_REQUEST)
            # output_dict = [x for x in data if x['type'] == '1']
            # values_arr = [x['_source']['play_name'] for x in data['hits']['hits']]
            # pprint(values_arr)
        except Exception as e:
            logger.error(str(e))
            return Response(
                            {'status': 'error',
                             'message': str(e),
                             'es_url': es_url,
                             'es_query': es_query},
                            status=status.HTTP_400_BAD_REQUEST)

        es_url_aliases = endpoint + "/_aliases"
        try:
            logger.info("requests.get url: " + es_url_aliases)
            start = time.time()
            es_search = requests.get(es_url_aliases)
            end = time.time()
            logger.info("Request execution %s", str(end - start))

            alias_list_json = es_search.json()
        except Exception as e:
            logger.error(str(e))
            return Response( {'status': 'error', 'message': str(e), 'es_url': es_url_aliases}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Getting mapping
        mappings_res = {}
        hits_arr = search['hits']['hits']
        for hit in hits_arr:
            index_name = hit['_index']
            if index_name not in mappings_res:
                es_url_mapping = endpoint + '/' + index_name + '/_mapping'
                try:
                    logger.info("requests.get url: %s", es_url_mapping)
                    start = time.time()
                    es_mapping = requests.get(es_url_mapping)
                    end = time.time()
                    logger.info("requests.get execution %s", str(end - start))

                    mapping = es_mapping.json()
                except Exception as e:
                    logger.error(str(e))
                    return Response({'status': 'error', 'message': str(e), 'es_url': es_url_mapping},
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
                # TODO проход по JSON элементам а не по массиву
                # [d[key] for key in d if d[key]['type']=='text']
                # d = mapping['shakespeare']['mappings']['act']['properties']
                # [d[key] for key in d if d[key].get('fields') is None]

            # es_mapping = requests.get(endpoint + "shakespeare?pretty")
            # mapping = es_mapping.json()


        #result['mapping'] = mappings_res
        data = search['hits']['hits']

        # enrich data to datasystem attributes and aliases
        for data_item in data:
            _index = data_item['_index']

            _type = data_item['_type']
            _source = data_item['_source']
            _new_source = {}

            try:
                data_item['_aliase'] = list(alias_list_json[_index]['aliases'].keys())[0]
            except Exception as e:
                # return Response('Aliase not found', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                data_item['_aliase'] = _index
                logger.warning('Aliase not found for %s ' % _index)

            for _field, _value in _source.items():

                if _field in mappings_res[_index][_type].keys():
                    fields_dict = mappings_res[_index][_type][_field]['fields']
                    for f in fields_dict:

                        if f not in _new_source.keys():
                            # _new_source[f] = [get_new_value(_source, _field, _value)]
                            _new_source[f] = [_source[_field]]
                        else:
                            # _new_source[f].append(get_new_value(_source, _field, _value))
                            _new_source[f].append(_source[_field])

                # else:
                    # _new_source[_field] = _value

            data_item['_data_system_source'] = _new_source

        result = {}
        # source_arr = [x['_source'] for x in search['hits']['hits']]
        result['data'] = data
        result['mapping_type'] = mapping_type.id


        return Response(result, status=status.HTTP_200_OK)
