from django.contrib import admin
from django.urls import path, include
from notifications.views import SendNotificationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),  # Importing user auth routes
    path('api/', include('location.urls')),
    path('notifications/', include('notifications.urls')),
    path('send-notification/', SendNotificationView.as_view(), name='send_notification'),
    path('events/', include('events.urls')),
]
