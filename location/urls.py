from django.urls import path
from location import views

urlpatterns = [
    path('venue',views.create_venue),
    path('event',views.create_event),
]

