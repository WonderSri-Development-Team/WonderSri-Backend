from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from .models import Event, Venue, Location
from .serializers import EventSerializer, VenueSerializer


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
        return Response({'error': 'Invalid latitude, longitude, or radius.'}, status=400)

    user_location = Point(user_longitude, user_latitude, srid=4326)

    nearby_events = Event.objects.annotate(
        distance=Distance('location__coordinates', user_location)
    ).filter(
        distance__lte=radius
    ).order_by('distance')

    serializer = EventSerializer(nearby_events, many=True)
    return Response(serializer.data)

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



