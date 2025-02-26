from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),# ✅ Importing user auth routes

    path('location/', include('location.urls')),
]
