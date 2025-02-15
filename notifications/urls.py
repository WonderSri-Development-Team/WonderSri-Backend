from django.urls import path
from .views import RegisterDeviceView

urlpatterns = [
    path('register-device/', RegisterDeviceView.as_view(), name='register_device')
]