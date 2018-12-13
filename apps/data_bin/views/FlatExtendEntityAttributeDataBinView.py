import json

from rest_framework import generics, status, views, viewsets
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.attribute.views import EntityAttributeMappingListView
from apps.auth_jwt.permissions import PublicEndpoint
from apps.data_bin.models import Bin, BinItem
from apps.data_bin.utils import (enrich_data, flatten, simplify_mapping,
                                 vice_versa_map)


class FlatExtendEntityAttributeDataBinView(views.APIView):
    """
    Get flatten and extended data from Items by Bin's Id (flat json mode)
    """
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        queryset = Bin.objects.all()
        user = self.request.user
        pk = self.kwargs['pk']
        bin = Bin.objects.get(pk=pk)

        # if user!=bin.user:
        #    return Response({'error':'you are not a bin\'s owner!'}, status=status.HTTP_403_FORBIDDEN)

        factory = APIRequestFactory()
        req = factory.get('/attribute/list-entity-attribute-mapping/')
        force_authenticate(req, user=user)
        view = EntityAttributeMappingListView.as_view()

        res = view(req)
        try:
            my_json = res.rendered_content.decode('utf8')
            entity_attribute_mapping = json.loads(my_json)
        except:
            entity_attribute_mapping = {}



        attr_to_entity_attr = vice_versa_map(entity_attribute_mapping)


        ids = []
        allData = []

        # distinct json
        for itemData in BinItem.objects.filter(bin=bin):
            mapping = itemData.mapping
            simple_mapping = simplify_mapping(mapping)

            simple_mapping_entity_attr = {}
            # turn attribute into entity attribute
            for key in simple_mapping:
                attr_list = simple_mapping[key]
                ent_attr_set = set()
                for attr in attr_list:
                    if attr in attr_to_entity_attr:
                        ent_attr_set.add(attr_to_entity_attr[attr])
                if len(ent_attr_set) > 0:
                    simple_mapping_entity_attr[key] = ent_attr_set

            #attr_to_entity_attr

            for item in itemData.data:
                id = item['_id']
                if id not in ids:
                    new_source = enrich_data(item, simple_mapping_entity_attr)
                    item['_source'] = new_source
                    allData.append(item)
                    ids.append(id)
            # allData.extend(itemData.data)

        # flatten json
        flatData = [
            flatten(data)
            for data in allData]
        # list = [
        # {'_id':item['_id'] for item in binItem.data}
        # binItem.data
        #    for binItem in BinItem.objects.filter(bin=bin)]

        # temp = [{'_id':1,'name':'n1'},{'_id':2,'name':'n2'}]

        return Response(flatData, status=status.HTTP_200_OK)
        # return Response(temp, status=status.HTTP_200_OK)
