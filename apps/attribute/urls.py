import logging

from django.conf.urls import url

from apps.attribute.models import MappingType
from backend import settings

from .views import (ActivateMappingTypeView, AttributeListView,
                    EntityAttributeListView, EntityAttributeMappingListView)

logger = logging.getLogger(__name__)

urlpatterns = [
    url(r'^activate-mapping-type/(?P<mapping_type_id>.+)$', ActivateMappingTypeView.as_view()),
    url(r'^list/$', AttributeListView.as_view()),
    url(r'^list-entity-attribute/$', EntityAttributeListView.as_view()),
    url(r'^list-entity-attribute-mapping/$', EntityAttributeMappingListView.as_view()),
]
