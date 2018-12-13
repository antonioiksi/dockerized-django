import logging

from rest_framework import status, views, viewsets
from rest_framework.response import Response

from apps.auth_jwt.permissions import PublicEndpoint
from apps.data_graph.models import GraphModelDrawing
from apps.data_graph.models.RelationTemplate import RelationTemplate

logger = logging.getLogger(__name__)


class CopyDefaultRelationTemplatesView(views.APIView):
    # create model template (one field model) for each attribute
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        defaultRelationTemplates = RelationTemplate.objects.filter(user=None)
        user = self.request.user

        count = 0
        countErr = 0
        for defaultRelationTemplate in defaultRelationTemplates:
            templates = RelationTemplate.objects.filter(user=user, name=defaultRelationTemplate.name)
            if len(templates) > 0:
                return Response({'status': 'error', 'message': 'Current user already has relation templates'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                relationTemplate = RelationTemplate(
                    user=user,
                    name=defaultRelationTemplate.name,
                    from_fields=defaultRelationTemplate.from_fields[:],
                    to_fields=defaultRelationTemplate.to_fields[:],
                    comparators=defaultRelationTemplate.comparators[:]
                )

                relationTemplate.save()
                count += 1
            except Exception as e:
                logger.warning('Error in creating  ModelTemplate: %s' % str(e))
                countErr += 1

        return Response({'status': 'success', 'message': 'created: %s, failed: %s' % (count, countErr)},
                        status=status.HTTP_200_OK)



class ClearRelationTemplateView(views.APIView):
    # delete all ModelTemplate objects for current user
    permission_classes = (PublicEndpoint,)

    def get(self, request, *args, **kwargs):
        user = self.request.user

        deleted = RelationTemplate.objects.filter(user=user).delete()

        return Response({'status': 'success', 'message': 'deleted: %s templates' % str(deleted)}, status=status.HTTP_200_OK)
