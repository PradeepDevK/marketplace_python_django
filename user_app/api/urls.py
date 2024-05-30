from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user_app.api.views import (
    registration_view,
    upload_excel,
    download_user_data
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', registration_view, name='register'),
    path('upload_excel/', upload_excel, name='upload_excel'),
    path('download_users/', download_user_data, name='download_users'),
]
