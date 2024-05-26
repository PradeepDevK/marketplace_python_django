from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/', include('marketplace_app.api.urls')),
    path('account/', include('user_app.api.urls')),
]
