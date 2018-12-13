from django.conf.urls import url

from apps.report.views.ReportView import ReportViewSet

urlpatterns = [
    url(r'^(?P<type>word|excel)$', ReportViewSet.as_view({'post': 'create'}), name='report'),
]
