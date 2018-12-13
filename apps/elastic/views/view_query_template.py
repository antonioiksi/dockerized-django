from rest_framework import generics

from apps.auth_jwt.permissions import PublicEndpoint
from apps.elastic.models import QueryTemplate
from apps.elastic.serializers import QueryTemplateSerializer


class QueryTemplateListView(generics.ListAPIView):
    """
    Return list of QueryTemplate objects
    """
    permission_classes = (PublicEndpoint,)
    serializer_class = QueryTemplateSerializer
    queryset = QueryTemplate.objects.all()
