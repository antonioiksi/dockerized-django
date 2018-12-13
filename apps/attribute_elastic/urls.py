from django.conf.urls import url

from .views import AddMappedFieldListView

urlpatterns = [

    url(r'^reload-mapped-attributes/(?P<mapping_type_id>.+)$', AddMappedFieldListView.as_view(), name='reload-mapped-attributes'),

]
