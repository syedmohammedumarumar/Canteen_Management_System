from django.urls import path
from .views import RegisterView, LogoutView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),  # ✅ only this
    path('logout/', LogoutView.as_view(), name='logout'),
]