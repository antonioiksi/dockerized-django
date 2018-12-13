from django.conf.urls import url

from .views import LoadExtendGraphFromBinView, LoadGraphFromBinView

urlpatterns = [

    url(r'^load/(?P<bin_pk>.+)/(?P<graph_pk>.+)$', LoadGraphFromBinView.as_view(), name='load'),

]
