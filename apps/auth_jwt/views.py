from django.contrib.auth.models import User
from django.shortcuts import render
# Create your views here.
from rest_framework import generics
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from apps.log.mixins import RequestLogViewMixin

from .serializers import UserSerializer


class TokenObtainPairWithLoggingView(RequestLogViewMixin, TokenObtainPairView):
    """
    Keep obtaining JWT token through Logging middleware.
    """


class TokenRefreshViewLoggingView(RequestLogViewMixin, TokenRefreshView):
    """
    Keep refreshing JWT token through Logging middleware.
    """


class CurrentUserView(RequestLogViewMixin, generics.ListAPIView):
    """
    Get current user info
    """
    serializer_class = UserSerializer
    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.pk)
