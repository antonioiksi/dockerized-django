from django.conf.urls import url

from .views import (ElasticSettingsByNameView, ElasticSettingsListMapView,
                    ElasticSettingsListView, ElasticSettingsResetByNameView,
                    ElasticSettingsUpdateSettingView,
                    ElasticSettingsUpdateView)

urlpatterns = [


    #url(r'^update/(?P<pk>.+)$', BinRetriveUpdateView.as_view(), name='update'),
    url(r'^list/$', ElasticSettingsListMapView.as_view(), name='list'),
    url(r'^list_/$', ElasticSettingsListView.as_view(), name='list'),

    url(r'^retrieve/(?P<name>.+)$', ElasticSettingsByNameView.as_view(), name='retrieve'),
    url(r'^reset/(?P<name>.+)$', ElasticSettingsResetByNameView.as_view(), name='reset'),

    url(r'^update-setting/(?P<name>.+)$', ElasticSettingsUpdateSettingView.as_view(), name='update-setting'),

    #url(r'^update/(?P<pk>.+)$', ElasticSettingsUpdateView.as_view(), name='update'),

]
