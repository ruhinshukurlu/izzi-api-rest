from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from authAPI.serializers import UserDetail
from authAPI.views import RegisterView, LoginView, RefreshTokenView, ChangePasswordView, UpdateUserView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('changePassword/<int:pk>/', ChangePasswordView.as_view()),
    path('refreshToken/', RefreshTokenView.as_view()),
    path('updateUser/<int:pk>/', UpdateUserView.as_view()),
    path('user/', UserDetailView.as_view()),
]
