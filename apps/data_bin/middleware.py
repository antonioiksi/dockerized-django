import datetime
import json
import logging
import socket
import time
from pprint import pprint

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from apps.attribute.models import Attribute, EntityAttribute

from .models import Bin, BinItem

logger = logging.getLogger(__name__)


def get_user_jwt(request):
    """
    Replacement for django session auth get_user & auth.get_user
     JSON Web Token authentication. Inspects the token for the user_id,
     attempts to get that user from the DB & assigns the user on the
     request object. Otherwise it defaults to AnonymousUser.

    This will work with existing decorators like LoginRequired  ;)

    Returns: instance of user object or AnonymousUser object
    """
    user = None
    try:
        user_jwt = JWTTokenUserAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            token_user = user_jwt[0]
            user_id = token_user.pk
            user = User.objects.get(id=user_id)
    except:
        pass
    return user


class BinItemDataEnrichFirstLevelMiddleware(object):
    """
    Received data enrich with First Level Attributes and save as Bin Items

    """

    def process_request(self, request):
        user = get_user_jwt(request)
        request.user = user
        logger.info(request.body.decode("utf-8"))
        request.start_time = time.time()

    def process_response(self, request, response):
        if request.method != 'POST' or 'data' not in response.data:
            return response

        # request.user
        user = request.user

        user_id = request.user.pk
        user = None
        if user_id is not None:
            user = User.objects.get(id=user_id)
        # response.data

        try:
            bin_pk = int(request.resolver_match.kwargs['bin_pk'])

            bin = Bin.objects.get(id=bin_pk)  # , user=user)
        except ObjectDoesNotExist:
            # response.status =
            return JsonResponse({'error': 'Bin with id=' + bin_pk + ' does not exist'}, 500)
            '''
            try:
                bin = Bin.objects.get(name='default', user=user)
                Bin.objects.filter(user=user).update(active=False)
                bin.active = True
                bin.save()
            except ObjectDoesNotExist:
                bin = Bin(user=user,
                          name='default',
                          active=True)
            '''

        # Bin.objects.filter(name='default',user=user.pk)

        jsonData = response.data
        data = jsonData['data']
        mapping_type = jsonData['mapping_type']
        # queryset = EntityAttribute.objects.filter(attributes__data_system=data_system_pk).values('name', 'attributes__name')

        first_level_mapping = {}

        if mapping_type == 0:
            queryset = EntityAttribute.objects.all().values('name')
            for row_queryset in queryset:
               attribute_name = row_queryset['name']
               first_level_mapping[attribute_name] = [attribute_name]


        else:
            queryset = Attribute.objects.filter(mapping_type=mapping_type).exclude(
                entity_attribute__isnull=True).values('name', 'entity_attribute__name')

            for row_queryset in queryset:
                attribute_name = row_queryset['name']
                entity_attribute_name = row_queryset['entity_attribute__name']
                if attribute_name in first_level_mapping.keys():
                    first_level_mapping[attribute_name].append(entity_attribute_name)
                else:
                    first_level_mapping[attribute_name] = [entity_attribute_name]

        # get mapping for current Data System
        # data_system = DataSystem.objects.get(pk=data_system_pk)

        for data_item in jsonData['data']:
            _data_system_source = data_item['_data_system_source']
            _first_level_source = {}
            for field_name in _data_system_source.keys():
                field_value = _data_system_source[field_name]
                if field_name in first_level_mapping.keys():
                    field_mapping_list = first_level_mapping[field_name]
                    for field_mapping_item in field_mapping_list:
                        if field_mapping_item not in _first_level_source.keys():
                            _first_level_source[field_mapping_item] = list(_data_system_source[field_name])
                        else:
                            _first_level_source[field_mapping_item].extend(_data_system_source[field_name])
                # else:
                # _new_source[field_name] = field_value

            data_item['_first_level_source'] = _first_level_source

            # mapping = None
        # if 'mapping' in response.data:
        #    mapping = jsonData['mapping']

        if mapping_type != 0:
            if len(request.body) > 0:
                query = json.loads(request.body.decode("utf-8"))
            else:
                query = None
        else:
            query = None

        url = request.path_info
        # pprint(data)
        item = BinItem(
            bin=bin,
            data=data,
            # mapping_type=mapping_type,
            query=query,
            # url=url
            datetime=datetime.datetime.now()
        )
        item.save()

        return response
