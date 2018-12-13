import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.data_graph.views.ModelTemplateView import \
    CopyDefaultModelTemplatesView
from apps.data_graph.views.RelationTemplateView import \
    CopyDefaultRelationTemplatesView

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def post_save_handler(sender, **kwargs):
    user = kwargs.get('instance', None)
    created = kwargs.get('created', None)

    logger.info(user.username)

    if created:
        factory = APIRequestFactory()
        request = factory.get('/graph/model-template/copy-default')
        force_authenticate(request, user=user)
        view = CopyDefaultModelTemplatesView.as_view()
        response = view(request)
        logger.info("Copying model templates %s " % str(response.data))

        request = factory.get('/graph/relation-template/copy-default')
        force_authenticate(request, user=user)
        view = CopyDefaultRelationTemplatesView.as_view()
        response = view(request)
        logger.info("Copying relation templates %s " % str(response.data))

    else:
        logger.info('update')
