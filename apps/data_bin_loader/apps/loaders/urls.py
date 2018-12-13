from django.conf.urls import url

from apps.data_bin_loader.apps.loaders.views import (CsvLoaderView,
                                                     JsonLoaderView)

urlpatterns = [
    url(r'^csv/$', CsvLoaderView.as_view(), name='csv'),
    url(r'^json/$', JsonLoaderView.as_view(), name='json'),
]
