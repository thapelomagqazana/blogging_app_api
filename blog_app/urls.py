from django.urls import path
from .views import UserRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),  # Login (JWT)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh
]