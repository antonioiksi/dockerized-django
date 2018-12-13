from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from apps.data_graph.views.GraphDataView import (ClearGraphDataView,
                                                 GraphDataAllKeysView,
                                                 GraphDataByModelNameView,
                                                 GraphDataList,
                                                 GraphDataRemoveItem,
                                                 JsonbFilterView,
                                                 LoadGraphDataView)
from apps.data_graph.views.GraphModelDrawingView import \
    GraphModelDrawingViewSet
from apps.data_graph.views.GraphModelView import (CopyGraphModelsFromTemplatesView,
                                                  GraphModelForGraphViewSet,
                                                  GraphModelViewSet)
from apps.data_graph.views.GraphNodeEdgeView import (GraphNodeEdgeAddForRelationsView,
                                                     GraphNodeEdgeClearView,
                                                     GraphNodeEdgeListView)
from apps.data_graph.views.GraphNodeView import (GraphNodeAddForModelsView,
                                                 GraphNodeClearView,
                                                 GraphNodeListView)
from apps.data_graph.views.GraphRelationView import (CopyGraphRelationsFromTemplatesView,
                                                     GraphRelationComparatorsView,
                                                     GraphRelationForGraphViewSet,
                                                     GraphRelationViewSet)
from apps.data_graph.views.GraphView import GraphViewSet
from apps.data_graph.views.ModelTemplateView import (ClearModelTemplateView,
                                                     CopyDefaultModelTemplatesView)
from apps.data_graph.views.RelationTemplateView import (ClearRelationTemplateView,
                                                        CopyDefaultRelationTemplatesView)

urlpatterns = [

    url(r'^clear/(?P<graph_id>.+)$', ClearGraphDataView.as_view(), name='clear'),
    url(r'^data/list/(?P<graph_id>.+)$', GraphDataList.as_view(), name='data-list'),

    url(r'^remove-data-from-graph/(?P<graph_id>.+)/(?P<id>.+)$', GraphDataRemoveItem.as_view(),
        name='remove-data-from-graph'),

    url(r'^load-data/(?P<graph_id>.+)$', LoadGraphDataView.as_view(), name='load-data'),

    url(r'^data-by-object-name/(?P<graph_name>.+)$', GraphDataByModelNameView.as_view(), name='data-by-name'),

    url(r'^node/remove-all/(?P<graph_id>.+)/$', GraphNodeClearView.as_view(), name='node-remove-all'),
    url(r'^node/list/(?P<graph_id>.+)/$', GraphNodeListView.as_view(), name='node-list'),
    url(r'^node/add/(?P<graph_id>.+)/$', GraphNodeAddForModelsView.as_view(), name='node-add'),

    url(r'^edge/remove-all/(?P<graph_id>.+)/$', GraphNodeEdgeClearView.as_view(), name='edge-remove-all'),
    url(r'^edge/list/(?P<graph_id>.+)/$', GraphNodeEdgeListView.as_view(), name='edge-list'),
    url(r'^edge/add/(?P<graph_id>.+)/$', GraphNodeEdgeAddForRelationsView.as_view(), name='edge-add'),

    # url(r'^object/(?P<object_name>.+)$', GraphObjectViewSet.as_view(), name='objects-by-name'),

    url(r'^all-keys/(?P<graph_id>.+)$', GraphDataAllKeysView.as_view(),
        name='all-keys'),
    url(r'^comparators/$', GraphRelationComparatorsView.as_view(),
        name='comparators'),

    url(r'^filter/$', JsonbFilterView.as_view(), name='filter'),

    url(r'^model/for-graph/(?P<graph_id>.+)$', GraphModelForGraphViewSet.as_view(), name='filter'),
    url(r'^model/copy-templates/(?P<graph_id>.+)$', CopyGraphModelsFromTemplatesView.as_view(), name='filter'),

    url(r'^relation/for-graph/(?P<graph_id>.+)$', GraphRelationForGraphViewSet.as_view(), name='filter'),
    url(r'^relation/copy-templates/(?P<graph_id>.+)$', CopyGraphRelationsFromTemplatesView.as_view(), name='filter'),

    url(r'^model-template/copy-default/$', CopyDefaultModelTemplatesView.as_view(), name='copy-default-model-template'),
    url(r'^model-template/clear/$', ClearModelTemplateView.as_view(), name='clear-model-template'),

    url(r'^relation-template/copy-default/$', CopyDefaultRelationTemplatesView.as_view(), name='copy-default-relation-template'),
    url(r'^relation-template/clear/$', ClearRelationTemplateView.as_view(), name='clear-relation-template'),

]

router = DefaultRouter()
router.register(r'graph', GraphViewSet, base_name='graph')
router.register(r'model', GraphModelViewSet, base_name='model')
router.register(r'drawing', GraphModelDrawingViewSet, base_name='drawing')
router.register(r'relation', GraphRelationViewSet, base_name='relation')
urlpatterns.extend(router.urls)
