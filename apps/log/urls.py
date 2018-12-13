from django.conf.urls import url

from apps.log.views import LogSearch, UserBinLogViewSet, UserListView

urlpatterns = [

    url(r'^$', LogSearch.as_view(), name='logs'),
    url(r'^user/(?P<user_id>(\d+))/$', LogSearch.as_view(), name='user-logs'),
    url(r'^date-from/(?P<date_from>(\d{4}-\d{2}-\d{2}))/date-to/(?P<date_to>(\d{4}-\d{2}-\d{2}))/$', LogSearch.as_view(), name='logs-date'),
    url(r'^user/(?P<user_id>(\d+))/date-from/(?P<date_from>(\d{4}-\d{2}-\d{2}))/date-to/(?P<date_to>(\d{4}-\d{2}-\d{2}))/$', LogSearch.as_view(), name='user-logs-date'),

    url(r'^users/$', UserListView.as_view(), name='users'),

]
