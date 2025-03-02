from django.urls import path
from location import views

urlpatterns = [
    path('venue',views.create_venue),
    path('event',views.create_event),
    path('nearby-events', views.list_nearby_events),
    path('activites', views.list_activities),
    path('acitivities/create', views.create_activity),

]

