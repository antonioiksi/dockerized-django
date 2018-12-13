import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
# Create your views here.
from rest_framework import exceptions, generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.auth_jwt.permissions import PublicEndpoint
from apps.data_bin.models import Bin
from apps.log.models import Log
from apps.log.serializers import (LogSearchSerializer, LogSerializer,
                                  LogUserSerializer)


class UserBinLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get list user search
    """
    permission_classes = (PublicEndpoint,)

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (JWTAuthentication,)

    # serializer_class = LogSerializer
    # model = Log

    def list(self, request):
        user = self.request.user

        user_id = self.kwargs.get('user_id', None)
        date_from = self.kwargs.get('date_from', None)
        date_to = self.kwargs.get('date_to', None)

        # queryset = Log.objects.filter(user=user, event__startswith='/data-bin-loader/').order_by('-datetime')
        queryset = Log.objects.filter(event__startswith='/data-bin-loader/')

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        if date_from is not None and date_to is not None:
            try:
                dt_from = datetime.datetime.strftime(date_from)
            except:
                return Response({'error': 'Bad param dt_from'}, status=status.HTTP_417_EXPECTATION_FAILED)

            try:
                dt_to = datetime.datetime.strftime(date_to)
            except:
                return Response({'error': 'Bad param dt_to'}, status=status.HTTP_417_EXPECTATION_FAILED)

            queryset = queryset.filter(user_id=user_id, datetime__range=(dt_from, dt_to))

            # queryset = Log.objects.filter(event__startswith='/data-bin-loader/').order_by('-datetime')

        res = []
        for log in queryset:
            try:
                if 'jsonQuery' in log.query.keys():
                    jsonQuery = log.query['jsonQuery']
                    bin_id = log.event.split('/')[3]
                    if bin_id == 32:
                        print('test')
                    try:
                        bin_name = Bin.objects.get(pk=bin_id).name
                    except:
                        bin_name = ''

                    if log.user_id > 0:
                        user_json = {
                            'id': log.user_id,
                            'name': log.user.username
                        }
                    else:
                        user_json = None

                    item = {
                        'user': user_json,
                        'event': log.event,
                        'bin_id': bin_id,
                        'bin_name': bin_name,
                        'jsonQuery': jsonQuery,
                        'datetime': log.datetime
                    }
                    res.append(item)
            except:
                print(log.query)

        # serializer = LogSerializer(queryset, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(res, status=status.HTTP_200_OK)


class LogSearch(generics.ListAPIView):
    permission_classes = (PublicEndpoint,)

    serializer_class = LogSearchSerializer

    # permission_classes = (IsAdminUser,)
    # ordering_fields = ('name',)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        date_from = self.kwargs.get('date_from', None)
        date_to = self.kwargs.get('date_to', None)

        filter_params = {"event__startswith": "/data-bin-loader/"}

        if user_id is not None:
            filter_params["user_id"] = user_id

        if date_from is not None and date_to is not None:
            try:
                dt_from = datetime.date(*map(int, date_from.split('-')))
            except:
                raise exceptions.ValidationError(detail='Bad param dt_from')

            try:
                dt_to = datetime.date(*map(int, date_to.split('-'))) + datetime.timedelta(days=1)
            except:
                raise exceptions.ValidationError(detail='Bad param dt_to')
            filter_params["datetime__range"] = (dt_from, dt_to)

        queryset = Log.objects.filter(**filter_params)

        return queryset


class UserListView(generics.ListAPIView):
    permission_classes = (PublicEndpoint,)
    serializer_class = LogUserSerializer
    # permission_classes = (IsAdminUser,)
    # ordering_fields = ('name',)

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
