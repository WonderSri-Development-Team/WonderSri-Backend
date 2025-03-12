from django.urls import path
from location import views

urlpatterns = [
    path('create-event',views.create_event),
    path('nearby-events', views.list_nearby_events),
    path('nearby-activites', views.list_nearby_activities),
    path('create-activities', views.create_activity),

]

