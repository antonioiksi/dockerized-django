from django.conf.urls import url

from apps.data_bin.views.BinItemDataView import (BinItemDataView,
                                                 FlatDataBinView,
                                                 RemoveRowFromDataView)
from apps.data_bin.views.BinItemView import (BinItemDeleteView,
                                             BinItemListView, BinItemView,
                                             UserItemsView)
from apps.data_bin.views.BinView import (ActiveBinRetrieveView,
                                         BinActivateView, BinCreateView,
                                         BinDeleteView, BinListView,
                                         BinResetView, BinUpdateView)
from apps.data_bin.views.FlatExtendEntityAttributeDataBinView import \
    FlatExtendEntityAttributeDataBinView

urlpatterns = [


    url(r'^activate/(?P<bin_pk>.+)$', BinActivateView.as_view(), name='activate'),
    url(r'^get-active/$', ActiveBinRetrieveView.as_view(), name='get-active'),


    url(r'^list/$', BinListView.as_view(), name='list'),
    url(r'^flat-data/(?P<pk>.+)$', FlatDataBinView.as_view(), name='flat-data'),
    url(r'^flat-extend-data/(?P<pk>.+)$', FlatExtendEntityAttributeDataBinView.as_view(), name='flat-extend-data'),

    url(r'^create/$', BinCreateView.as_view(), name='create'),
    url(r'^update/(?P<pk>.+)$', BinUpdateView.as_view(), name='update'),
    url(r'^delete/(?P<pk>.+)$', BinDeleteView.as_view(), name='delete'),

    url(r'^reset/(?P<pk>.+)$', BinResetView.as_view(), name='reset'),

    url(r'^user-items/$', UserItemsView.as_view(), name='user-items'),
    url(r'^(?P<bin_pk>.+)/items/data/$', BinItemDataView.as_view(), name='bin-items-data'),

    url(r'^items/data/remove/$', RemoveRowFromDataView.as_view(), name='items-data-remove'),


    url(r'^item/list/(?P<bin_pk>.+)$', BinItemListView.as_view(), name='bin-item-list'),
    url(r'^item/(?P<pk>.+)$', BinItemView.as_view(), name='bin-item'),
    url(r'^item/delete/(?P<pk>.+)$', BinItemDeleteView.as_view(), name='bin-item-delete'),

    #url(r'^update/(?P<pk>.+)$', BinRetriveUpdateView.as_view(), name='update'),
    #url(r'^list/$', BinViewSet.as_view({'get': 'list'}), name='list'),
    #url(r'^retrieve/(?P<pk>.+)$', BinViewSet.as_view({'get': 'retrieve'}), name='retrieve'),


]
