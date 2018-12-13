from django.shortcuts import render
# Create your views here.
from rest_framework import generics, renderers, status, views
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.auth_jwt.permissions import PublicEndpoint

from .models import Attribute, EntityAttribute, MappingType
from .serializers import (AttributeSerializer, EntityAttributeSerializer,
                          EntityAttributeSimpleSerializer,
                          MappingTypeSerializer)


class ActivateMappingTypeView(views.APIView):
    """
    Activate 'Mapping Type' for seraching
    """
    def put(self, request, mapping_type_id):
        try:
            mapping_type = MappingType.objects.get(pk=mapping_type_id)
        except MappingType.DoesNotExist:
            raise NotFound(detail='Object Bin not found', code=None)

        MappingType.objects.update(active=False)
        mapping_type.active = True
        mapping_type.save()
        serializer = MappingTypeSerializer(mapping_type)

        from apps.attribute.utils import update_ELASTIC_SEARCH_URL
        update_ELASTIC_SEARCH_URL()

        return Response(serializer.data, status=status.HTTP_200_OK)


class AttributeListView(generics.ListAPIView):
    """
    Get list of attribute (attribute is the same as field name)
    """
    permission_classes = (PublicEndpoint,)
    serializer_class = AttributeSerializer
    queryset = Attribute.objects.all()


class EntityAttributeListView(generics.ListAPIView):
    """
    Get list of search attribute
    """
    permission_classes = (PublicEndpoint,)
    serializer_class = EntityAttributeSerializer
    queryset = EntityAttribute.objects.all().order_by('order')


class CustomRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        result = {}
        for item in data:
            result['name'] = item['name']
            result['title'] = item['title']
            attr_list = item['attributes']
            attr_list2 = []
            for attr in attr_list:
                attr_list2.append(attr['name'])
            result['attributes'] = attr_list2

        data = result
        return super(CustomRenderer, self).render(data, accepted_media_type, renderer_context)


class EntityAttributeCustomListView(generics.ListAPIView):
    """
    Get list of search attribute
    """
    # permission_classes = (PublicEndpoint,)
    serializer_class = EntityAttributeSerializer
    queryset = EntityAttribute.objects.all()
    renderer_classes = (CustomRenderer, renderers.BrowsableAPIRenderer)


class MappingRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        result = {}
        for item in data:
            search_attr_name = item['name']
            # result['title'] = item['title']
            attr_list = item['attributes']
            attr_list2 = []
            for attr in attr_list:
                attr_list2.append(attr['name'])
            result[search_attr_name] = attr_list2

        data = result
        return super(MappingRenderer, self).render(data, accepted_media_type, renderer_context)


class EntityAttributeMappingListView(generics.ListAPIView):
    """
    Get list of search attribute
    """
    # permission_classes = (PublicEndpoint,)
    serializer_class = EntityAttributeSerializer
    queryset = EntityAttribute.objects.all()
    renderer_classes = (MappingRenderer, renderers.BrowsableAPIRenderer)
