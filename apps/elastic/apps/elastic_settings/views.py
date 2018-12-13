from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
# Create your views here.
from django.views.generic import UpdateView
from rest_framework import generics, serializers, status, views
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from apps.auth_jwt.permissions import PublicEndpoint

from .models import ElasticSettings
from .serializers import ElasticSettingsSerializer


class ElasticSettingsListView(generics.ListAPIView):
    """
    Return 'ElasticSettings' list for user, if setting doesnot exit, then clone from User=None
    """
    serializer_class = ElasticSettingsSerializer
    permission_classes = (PublicEndpoint,)
    #permission_classes = (IsAdminUser,)
    ordering_fields = ('name',)

    def get_queryset(self):
        user = self.request.user
        querysetDefault = ElasticSettings.objects.filter(user=None)
        setting_names = []
        for defaultSetting in querysetDefault:
            name = defaultSetting.name
            queryset = ElasticSettings.objects.filter(user=user, name=name)
            if len(queryset) == 0:
                elasticSetting = ElasticSettings(name=defaultSetting.name,
                                                 title=defaultSetting.title,
                                                setting=defaultSetting.setting,
                                                user=user)
                elasticSetting.save()
        queryset = ElasticSettings.objects.filter(user=user)
        return queryset


class ElasticSettingsByNameView(generics.ListAPIView):
    """
    Return 'ElasticSettings' item by name
    """
    serializer_class = ElasticSettingsSerializer
    permission_classes = (PublicEndpoint,)
    #permission_classes = (IsAdminUser,)

    def get_queryset(self):
        name = self.kwargs['name']
        user = self.request.user
        queryset = ElasticSettings.objects.filter(user=user, name=name)
        if len(queryset)==0:
            queryset = ElasticSettings.objects.filter(user=None, name=name)
            if len(queryset)==0:
                raise Http404("Setting with name %s does not supported", name)

            elasticSettingUserNone = queryset[0]
            elasticSetting = ElasticSettings(name=elasticSettingUserNone.name,
                                             title=elasticSettingUserNone.title,
                                             setting=elasticSettingUserNone.setting,
                                             user=user)
            instance = elasticSetting.save()
            return instance
        return queryset



class ElasticSettingsListMapView(views.APIView):
    """
    Return 'ElasticSettings' item by name
    """
    #serializer_class = ElasticSettingsSerializer
    permission_classes = (PublicEndpoint,)
    #permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        querysetDefault = ElasticSettings.objects.filter(user=None)
        setting_names = []
        for defaultSetting in querysetDefault:
            name = defaultSetting.name
            queryset = ElasticSettings.objects.filter(user=user, name=name)
            if len(queryset) == 0:
                elasticSetting = ElasticSettings(name=defaultSetting.name,
                                                 title=defaultSetting.title,
                                                setting=defaultSetting.setting,
                                                user=user)
                elasticSetting.save()
        queryset = ElasticSettings.objects.filter(user=user)
        mapUserSettings = {item.name: ElasticSettingsSerializer(item).data for item in queryset}

        #serializer = ElasticSettingsSerializer(elasticSetting)
        return Response(mapUserSettings, status=status.HTTP_200_OK)



class ElasticSettingsResetByNameView(views.APIView):
    """
    Return 'ElasticSettings' item by name
    """
    #serializer_class = ElasticSettingsSerializer
    permission_classes = (PublicEndpoint,)
    #permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        name = self.kwargs['name']
        user = self.request.user
        querysetUserNone = ElasticSettings.objects.filter(user=None, name=name)
        if len(querysetUserNone) == 0:
            raise Http404("Setting with name %s does not supported", name)
        elasticSettingUserNone = querysetUserNone[0]

        queryset = ElasticSettings.objects.filter(user=user, name=name)
        if len(queryset)==0:
            queryset = ElasticSettings.objects.filter(user=None, name=name)
            if len(queryset)==0:
                raise Http404("Setting with name %s does not supported", name)

            elasticSetting = ElasticSettings(name=elasticSettingUserNone.name,
                                             title=elasticSettingUserNone.title,
                                             setting=elasticSettingUserNone.setting,
                                             user=user)
            elasticSetting.save()

        else:
            elasticSetting = queryset[0]
            elasticSetting.setting = elasticSettingUserNone.setting
            elasticSetting.save()

        #elasticSetting
        serializer = ElasticSettingsSerializer(elasticSetting)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #return

        #return elasticSetting


class ElasticSettingsUpdateView(generics.UpdateAPIView):
    # TODO doesn't work properly!!!
    serializer_class = ElasticSettingsSerializer
    def perform_update(self, serializer):
        serializer.save()


class ElasticSettingsUpdateSettingView(views.APIView):
    permission_classes = (PublicEndpoint,)
    #serializer_class = ElasticSettingsSerializer

    def post(self, request, *args, **kwargs):
        newSetting = request.data # json.loads(request.body.decode("utf-8"))
        #json.dumps(request.data)
        name = self.kwargs['name']
        user = self.request.user
        elasticSetting = ElasticSettings.objects.get(user=user, name=name)
        # check user
        if elasticSetting.user==None:
            raise Http404("You could not change default settings!")
        if user != elasticSetting.user:
            raise Http404("You could not change friends settings!")

        elasticSetting.setting = newSetting
        elasticSetting.save()

        serializer = ElasticSettingsSerializer(elasticSetting)
        #return Response(json.dumps( serializer.data, ensure_ascii=False), status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


'''
class ElasticSettingsUpdateView(views.APIView):
    permission_classes = (PublicEndpoint,)

    def post(self, request, *args, **kwargs):
        #source_arr = [x['_source'] for x in data['hits']['hits']]
        user = self.request.user
        ElasticSettings.objects.filter(user=user, name=)
        
        r = requests.post(settings.ELASTIC_SEARCH_URL+"/_search?size="+settings.ELASTIC_SEARCH_RESULT_NUMBER,
                          json.dumps(request.data))
        search = r.json()

        if r.status_code == 200:
            result = {}
            result['data'] = search['hits']['hits']

            return Response( result, status=status.HTTP_200_OK)
        else:
            return Response('app_elastic error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #raise APIException("There was a problem!")
'''
