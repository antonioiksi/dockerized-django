import logging

from backend import settings

logger = logging.getLogger(__name__)

def update_ELASTIC_SEARCH_URL():
    from apps.attribute.models import MappingType

    try:
        # MappingType.objects.all()
        mapping_type = MappingType.objects.filter(active=True)[0]
        logger.info('Update  settings.ELASTIC_SEARCH_URL, %s' % mapping_type.endpoint)
        settings.ELASTIC_SEARCH_URL = mapping_type.endpoint
    except Exception as ex:
        logger.error('No MappingType was found. Please add MappingType and check Attributes')
        # raise Exception('No MappingType was found. Please add MappingType and check Attributes')
