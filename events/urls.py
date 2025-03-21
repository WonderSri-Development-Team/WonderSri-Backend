from django.urls import path
from .views import check_nearby_events

urlpatterns = [
    path('check-events/', check_nearby_events, name="check-events"),
]