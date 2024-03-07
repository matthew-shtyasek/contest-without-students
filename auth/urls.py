from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from auth.serializers import AuthTokenSerializer
from auth.views import RegisterAPIView, LogoutAPIView


app_name = 'custom_auth'


urlpatterns = [
    path('login/', ObtainAuthToken.as_view(serializer_class=AuthTokenSerializer), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout')
]
