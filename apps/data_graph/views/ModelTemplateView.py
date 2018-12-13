import logging

from rest_framework import status, views, viewsets
from rest_framework.response import Response

from apps.attribute.models import EntityAttribute
from apps.auth_jwt.permissions import PublicEndpoint
from apps.data_graph.models import GraphModelDrawing
from apps.data_graph.models.Graph import Graph
from apps.data_graph.models.ModelTemplate import ModelTemplate
from apps.data_graph.serializers.GraphSerializer import GraphSerializer

logger = logging.getLogger(__name__)


class CopyDefaultModelTemplatesView(views.APIView):
    """
    If current user has no model templates than
    copy them from "none" user templates
    """
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        defaultModelTemplates = ModelTemplate.objects.filter(user=None)
        user = self.request.user

        count = 0
        countErr = 0
        for defaultModelTemplate in defaultModelTemplates:
            templates = ModelTemplate.objects.filter(user=user, name=defaultModelTemplate.name)
            if len(templates) > 0:
                return Response({'status': 'error', 'message': 'Current user already has model templates'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                modelTemplate = ModelTemplate(
                    user=user,
                    name=defaultModelTemplate.name,
                    fields=defaultModelTemplate.fields[:],
                    is_group=defaultModelTemplate.is_group,
                    drawing=defaultModelTemplate.drawing
                )

                modelTemplate.save()
                count += 1
            except Exception as e:
                logger.warning('Error in creating  ModelTemplate: %s' % str(e))
                countErr += 1

        return Response({'status': 'success', 'message': 'created: %s, failed: %s' % (count, countErr)},
                        status=status.HTTP_200_OK)


class ClearModelTemplateView(views.APIView):
    """
    Remove all model templates for current user
    """
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        user = self.request.user

        deleted = ModelTemplate.objects.filter(user=user).delete()

        return Response({'status': 'success', 'message': 'deleted: %s templates' % str(deleted)}, status=status.HTTP_200_OK)
