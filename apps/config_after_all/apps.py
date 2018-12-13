import logging

from django.apps import AppConfig
from rest_framework.test import APIRequestFactory, force_authenticate

from backend import settings

logger = logging.getLogger(__name__)


class ConfigAfterAllConfig(AppConfig):
    name = "apps.config_after_all"
    label = "apps.config_after_all"
    verbose_name = "ConfigAfterAll Config App"

    def ready(self):
        logger.info('ConfigAfterAllConfig')

        from apps.attribute.models import MappingType
        try:
            # MappingType.objects.all()
            active_mapping_type = MappingType.objects.filter(active=True)[0]
            logger.info('Current active MappingType %s' % active_mapping_type.id)
        except Exception as ex:
            logger.error('No MappingType was found. Please add MappingType and check Attributes')
            # raise Exception('No MappingType was found. Please add MappingType and check Attributes')

        from django.contrib.auth.models import User
        user = User.objects.get(pk=1)
        logger.info(user.username)
        # from apps.attribute.models import MappingType
        mapping_types = MappingType.objects.all()
        for mapping_type in MappingType.objects.all():
            factory = APIRequestFactory()

            # Activate MappingType
            request = factory.put('/attribute/activate-mapping-type/%s' % mapping_type.id)
            force_authenticate(request, user=user)
            from apps.attribute.views import ActivateMappingTypeView
            view = ActivateMappingTypeView.as_view()
            response = view(request, mapping_type_id=mapping_type.id)
            logger.info("Activated mapping_type %s: %s " % (mapping_type.id, str(response.data)))

            try:
                # Find and add new attributes
                request = factory.get('/attribute/reload-mapped-attributes/%s' % mapping_type.id)
                force_authenticate(request, user=user)
                from apps.attribute_elastic.views import AddMappedFieldListView
                view = AddMappedFieldListView.as_view()
                response = view(request, mapping_type_id=mapping_type.id)
                logger.info("Copying new attributes for mapping_type %s: %s " % (mapping_type.id, str(response.data)))
            except Exception as e:
                logger.error("Error updating attribute for mapping_type %s: %s " % (mapping_type.id, str(e)))

        # return active MappingType
        if active_mapping_type is not None:
            request = factory.put('/attribute/activate-mapping-type/%s' % active_mapping_type.id)
            force_authenticate(request, user=user)
            from apps.attribute.views import ActivateMappingTypeView
            view = ActivateMappingTypeView.as_view()
            response = view(request, mapping_type_id=active_mapping_type.id)
            logger.info("Activated mapping_type %s: %s " % (active_mapping_type.id, str(response.data)))
        else:
            logger.error('No active MappingType was found. Please activate MappingType manually')
