from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from .models import Event, Venue, Location, Activities
from .serializers import EventSerializer, VenueSerializer, ActivitiesSerializer


@swagger_auto_schema(
    method='GET',
    responses={
        '200': EventSerializer(many=True),
        '400': 'Bad request',
    }
)
@api_view(['GET'])
def list_nearby_events(request):
    """
    Lists nearby events within a given radius.
    """
    user_latitude = request.GET.get('lat')
    user_longitude = request.GET.get('lon')
    radius = request.GET.get('radius', 10000)  # Optional radius, default 10km

    try:
        user_latitude = float(user_latitude)
        user_longitude = float(user_longitude)
        radius = float(radius)
    except (TypeError, ValueError):
        return Response({'error': 'Invalid latitude, longitude, or radius.'}, status=status.HTTP_400_BAD_REQUEST)

    user_location = Point(user_longitude, user_latitude, srid=4326)

    nearby_events = Event.objects.annotate(
        distance=Distance('venue__location__coordinates', user_location)  # Ensure correct field reference
    ).filter(
        distance__lte=radius
    ).order_by('distance')

    serializer = EventSerializer(nearby_events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    operation_description="Create a new event",
    request_body=EventSerializer,
    responses={
        201: EventSerializer,
        400: "Bad Request",
    }
)
@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def create_event(request):
    """
    Create a new event.
    """
    serializer = EventSerializer(data=request.data)

    if serializer.is_valid():
        # Save the event (including nested location and venue)
        event = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Create a new venue",
    request_body=VenueSerializer,
    responses={
        201: VenueSerializer,
        400: "Bad Request",
    }
)
@api_view(['POST'])
def create_venue(request):
    """
    Create a new venue.
    """
    serializer = VenueSerializer(data=request.data)


    if serializer.is_valid():
        venue = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={
        200: ActivitiesSerializer,
        400: "Bad Request",
    }
)
  # Ensure you create this serializer
@api_view(['GET'])
def list_activities(request):
    """
    List activities around a specific location.
    """
    venue_id = request.GET.get('venue_id')
    if venue_id:
        activities = Activities.objects.filter(venue_id=venue_id)
    else:
        activities = Activities.objects.all()  # Return all activities if no filter is applied

    serializer = ActivitiesSerializer(activities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    request_body=ActivitiesSerializer,
    responses={
        201: ActivitiesSerializer,
        400: "Bad Request",
    }
)
@api_view(['POST'])
def create_activity(request):
    """
    Create a new activity.
    """
    serializer = ActivitiesSerializer(data=request.data)
    if serializer.is_valid():
        activity = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




