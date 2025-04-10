from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from .views import RegisterCreateAPIView, LoginCreateAPIView,EmailTokenObtainPairView


urlpatterns = [
    path('register/', RegisterCreateAPIView.as_view(), name="token_obtain_pair"),
    path('login/', LoginCreateAPIView.as_view(), name="token_obtain_pair"),
    path('token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]