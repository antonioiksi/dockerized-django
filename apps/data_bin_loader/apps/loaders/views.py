import datetime
import json

from rest_framework import status, views
from rest_framework.response import Response

from apps.attribute.models import EntityAttribute
from apps.auth_jwt.permissions import PublicEndpoint
from apps.log.mixins import RequestLogViewMixin


class JsonLoaderView(RequestLogViewMixin, views.APIView):
    """

    """
    permission_classes = (PublicEndpoint,)

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body.decode("utf-8"))

        # load entity attributes
        first_level_mapping = {}
        queryset = EntityAttribute.objects.all().values('name')
        for row_queryset in queryset:
            attribute_name = row_queryset['name']
            first_level_mapping[attribute_name] = [attribute_name]

        result = []
        for item in json_data:
            res_item = {}
            if '_id' not in item.keys():
                res_item['_id'] = datetime.datetime.now().microsecond
            else:
                res_item['_id'] = item['_id']
            res_item['_source'] = item
            # res_item['_data_system_source'] = item
            result.append(res_item)


        for data_item in result:
            #_source = data_item['_source']
            _source = data_item['_source']
            _data_system_source = {}
            for field_name in _source.keys():
                field_value = _source[field_name]
                if field_name in first_level_mapping.keys():
                    field_mapping_list = first_level_mapping[field_name]
                    for field_mapping_item in field_mapping_list:
                        if field_mapping_item not in _data_system_source.keys():
                            _data_system_source[field_mapping_item] = [_source[field_name]]
                        else:
                            _data_system_source[field_mapping_item].extend(_source[field_name])
                # else:
                # _new_source[field_name] = field_value

            data_item['_data_system_source'] = _data_system_source


        _source1 = {'phone': '322223322', 'patronomic_name': 'ssp'}
        _source11 = {'phone': ['322223322']}
        _source2 = {'person_name': 'Petrov', 'musor': 'value musor'}
        _source22 = {'person_name': ['Petrov']}

        result = {
                    # 'data': [
                    #         {
                    #             '_id': 1,
                    #             '_source': _source1,
                    #             '_data_system_source': _source11},
                    #         {
                    #             '_id': 2,
                    #             '_source': _source2,
                    #             '_data_system_source': _source22},
                    #         ],
                    'data': result,
                    'mapping_type': 0}

        return Response(result, status=status.HTTP_200_OK)



class CsvLoaderView(RequestLogViewMixin, views.APIView):
    """

    """
    permission_classes = (PublicEndpoint,)

    def post(self, request, *args, **kwargs):
        _source1 = {'phone': '322223322', 'patronomic_name': 'ssp'}
        _source11 = {'phone': ['322223322']}
        _source2 = {'person_name': 'Petrov', 'musor': 'value musor'}
        _source22 = {'person_name': ['Petrov']}

        result = {'data': [
                            {
                                '_id': 1,
                                '_source': _source1,
                                '_data_system_source': _source11},
                            {
                                '_id': 2,
                                '_source': _source2,
                                '_data_system_source': _source22},
                            ],
                  'mapping_type': 0}

        return Response(result, status=status.HTTP_200_OK)
