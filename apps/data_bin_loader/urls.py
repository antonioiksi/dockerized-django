from django.conf.urls import url

from .views import CsvView, DataBinSimpleSearchView, ElasticView, JsonView

urlpatterns = [


    url(r'^elastic/(?P<bin_pk>.+)$', ElasticView.as_view(), name='elastic'),

    url(r'^json/(?P<bin_pk>.+)$', JsonView.as_view(), name='json'),
    url(r'^csv/(?P<bin_pk>.+)$', CsvView.as_view(), name='csv'),

    # url(r'^simple-search/$', DataBinSimpleSearchView.as_view(), name='simple-search'),

]
