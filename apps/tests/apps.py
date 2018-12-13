import logging

from django.apps import AppConfig

# from apps.attribute.models import MappingType
from backend import settings

logger = logging.getLogger(__name__)


class TestsConfig(AppConfig):
    name = 'apps.tests'

    def ready(self):
        logger.info('TestsConfig')
        # from apps.attribute.models import MappingType
        #
        # try:
        #     # MappingType.objects.all()
        #     mapping_type = MappingType.objects.filter(active=True)[0]
        #     logger.info('Update  settings.ELASTIC_SEARCH_URL, %s' % mapping_type.endpoint)
        #     settings.ELASTIC_SEARCH_URL = mapping_type.endpoint
        # except Exception as ex:
        #     logger.error(str(ex))
