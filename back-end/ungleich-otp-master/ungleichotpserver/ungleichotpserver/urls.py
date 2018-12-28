from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from otpauth.views import OTPVerifyViewSet
from user_management.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'ungleichotp', OTPVerifyViewSet, basename='ungleichotp')
router.register(r'usermanagement', UserViewSet, basename='usermanagement')
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
