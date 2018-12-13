from django.conf.urls import url
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (CurrentUserView, TokenObtainPairWithLoggingView,
                    TokenRefreshViewLoggingView)

urlpatterns = [

    # JWT authentification
    url(r'^token/obtain/$', TokenObtainPairWithLoggingView.as_view()),
    url(r'^token/refresh/$', TokenRefreshViewLoggingView.as_view()),
    url(r'^token/verify/$', TokenVerifyView.as_view()),
    url(r'^token/user-info/$', CurrentUserView.as_view()),

]
