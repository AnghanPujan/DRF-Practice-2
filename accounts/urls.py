from django.urls import path
from .views import LoginAPIView, RegisterAPIView, UserCreateView, SuperAdminDashboard

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('createuser/', UserCreateView.as_view(), name="createuser"),
    path('adminDashboard/', SuperAdminDashboard.as_view(), name='superDashboard')
]   