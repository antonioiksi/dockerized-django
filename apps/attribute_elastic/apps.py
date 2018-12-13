import logging

from django.apps import AppConfig
from rest_framework.test import APIRequestFactory, force_authenticate

# from apps.attribute_elastic.views import AddMappedFieldListView

logger = logging.getLogger(__name__)


class AttributeElasticConfig(AppConfig):
    name = 'apps.attribute_elastic'

    def ready(self):
        logger.info('AttributeElasticConfig')
