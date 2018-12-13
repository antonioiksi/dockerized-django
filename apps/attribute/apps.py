import logging

import django
from django.apps import AppConfig

# django.setup()
# from apps.attribute.models import MappingType
from backend import settings

logger = logging.getLogger(__name__)

class AttributeConfig(AppConfig):
    name = 'apps.attribute'

    def ready(self):
        logger.info('AttributeConfig')
        # from apps.attribute.models import MappingType
        # # MappingType.objects.all()
        # try:
        #     mapping_type = MappingType.objects.filter(active=True)
        # except Exception as ex:
        #      logger.error(str(ex))
        # logger.info('Update  settings.ELASTIC_SEARCH_URL, %s' % mapping_type.endpoint)
        # settings.ELASTIC_SEARCH_URL = mapping_type.endpoint
