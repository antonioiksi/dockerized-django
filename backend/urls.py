"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views import generic
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_swagger_view(title='Rest API docs with Swagger')

urlpatterns = [
    # redirect
    url(r'^$', generic.RedirectView.as_view(url='/admin/', permanent=False)),
    url(r'^admin/', admin.site.urls),

    url(r'^api/$', get_schema_view()),

    url(r'^docs/', include_docs_urls(title='Rest API docs')),
    url(r'^docs/swagger/', schema_view),

    # JWT authentification
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth/', include('apps.auth_jwt.urls', namespace='auth_jwt')),

    url(r'^tests/', include('apps.tests.urls', namespace='tests')),
    url(r'^git/', include('apps.git.urls', namespace='git')),

    #
    url(r'^attribute/', include('apps.attribute.urls', namespace='attribute')),
    url(r'^attribute/', include('apps.attribute_elastic.urls', namespace='attribute-elastic')),

    #
    url(r'^bin/', include('apps.data_bin.urls', namespace='bin')),
    url(r'^graph/', include('apps.data_graph.urls', namespace='graph')),

    url(r'^bin-graph/', include('apps.data_bin_data_graph.urls', namespace='bin-graph')),
    #
    url(r'^elastic/', include('apps.elastic.urls', namespace='elastic')),

    url(r'^elastic/settings/', include('apps.elastic.apps.elastic_settings.urls', namespace='elastic_settings')),

    #
    url(r'^data-bin-loader/', include('apps.data_bin_loader.urls', namespace='data-bin-loader')),
    url(r'^', include('apps.data_bin_report.urls', namespace='data-bin-report')),

    url(r'^report/', include('apps.report.urls', namespace='report')),

    url(r'^log/', include('apps.log.urls', namespace='log')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
