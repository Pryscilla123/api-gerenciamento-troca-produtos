from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from base_app.serializers import ChangePasswordSerializer
from base_app.views import UserViewSets, ChangePasswordView, ResetPasswordView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserViewSets.as_view(), name='user-list-create'),
    path('api/change_password/', ChangePasswordView.as_view(),
         name='change-password'),
    path('api/reset_password/', ResetPasswordView.as_view()),
]
