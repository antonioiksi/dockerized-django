import json
import logging

import requests
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, RequestsClient

from apps.attribute.models import Attribute, MappingType
from apps.attribute.serializers import AttributeSerializer
from apps.auth_jwt.permissions import PublicEndpoint
from apps.elastic.views.view_mapped_field_list import MappedFieldListView
from apps.log.mixins import RequestLogViewMixin
from backend import settings

logger = logging.getLogger(__name__)


class AddMappedFieldListView(RequestLogViewMixin, views.APIView):
    """

    """

    # permission_classes = (PublicEndpoint,)

    def get(self, request, mapping_type_id):
        try:
            mapping_type = MappingType.objects.get(pk=mapping_type_id)
        except ObjectDoesNotExist as e:
            return Response({'status': 'error', 'message': 'No MappingType with id: %s' % mapping_type_id, }, status=status.HTTP_400_BAD_REQUEST)



        try:
            request = APIRequestFactory().get('/elastic/mapped-field-list/')
            response = MappedFieldListView.as_view()(request).render()
            response_json = json.loads(response.content.decode('utf8'))

            # output_dict = [x for x in data if x['type'] == '1']
            # values_arr = [x['_source']['play_name'] for x in data['hits']['hits']]
            # pprint(values_arr)
        except Exception as e:
            return Response({'status': 'error', 'message': 'app_elastic error: %s' % e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Attribute.objects.all().delete()
        found = 0
        added = 0
        for key in response_json.keys():
            # print('key'+key)
            found += 1
            if Attribute.objects.filter(name=key, mapping_type=mapping_type).count() == 0:
                Attribute(name=key, mapping_type=mapping_type).save()
                added += 1

        return Response({'status': 'success', 'message': 'found: %s add: %s' % (found, added)}, status=status.HTTP_200_OK)
