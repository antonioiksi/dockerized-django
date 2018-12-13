import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class DataGraphConfig(AppConfig):
    name = "apps.data_graph"

    def ready(self):
        logger.info('DataGraphConfig')
        import apps.data_graph.signals
