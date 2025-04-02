from django.contrib import admin
from django.urls import path, include
from notifications.views import SendNotificationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    path('location/', include('location.urls')),
    path('notifications/', include('notifications.urls')),
]
