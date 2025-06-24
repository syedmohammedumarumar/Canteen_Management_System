from django.urls import path
from .views import RegisterView, CustomAuthToken, CustomerProfileView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('profile/', CustomerProfileView.as_view(), name='profile'),
     path('api/token/', obtain_auth_token, name='api_token_auth'),
]