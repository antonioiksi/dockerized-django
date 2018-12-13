from django.conf.urls import url

from apps.git.views import GitVersionView

urlpatterns = [

    url(r'^version/$', GitVersionView.as_view(), name='version'),

]
