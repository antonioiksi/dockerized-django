from django.conf.urls import url

from apps.elastic.views.ESInfoView import ESInfoView
from apps.elastic.views.view_count import CountDocsView

from .views.view_aliase_list import AliasListView
from .views.view_drill_search import DrillSearchView
from .views.view_mapped_field_list import MappedFieldListView
from .views.view_mapped_search import MappedSearchView
from .views.view_query_template import QueryTemplateListView
from .views.view_simple_search import SimpleSearchView

urlpatterns = [


    url(r'^info/$', ESInfoView.as_view(), name='info'),
    url(r'^simple-search/$', SimpleSearchView.as_view(), name='simple-search'),
    url(r'^mapped-search/$', MappedSearchView.as_view(), name='mapped-search'),
    url(r'^alias-list/$', AliasListView.as_view(), name='alias-list'),
    url(r'^mapped-field-list/$', MappedFieldListView.as_view(), name='mapped-field-list'),

    url(r'^query-template/list/$', QueryTemplateListView.as_view(), name='query-template-list'),

    url(r'^count/$', CountDocsView.as_view(), name='count'),

]
