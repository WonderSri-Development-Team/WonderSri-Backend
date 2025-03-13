from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from .models import Event, Activity, Food
from .serializers import EventSerializer, FoodSerializer, ActivitiesSerializer


# --------------------------- LOCATION-BASED EVENTS ---------------------------


@swagger_auto_schema(
    method='GET',
    responses={200: EventSerializer(many=True), 400: "Bad request"},
)
@api_view(['GET'])
def list_nearby_events(request):
    """
    Lists nearby events **sorted by distance** from the user's location.
    """
    user_latitude = request.GET.get('lat')
    user_longitude = request.GET.get('lon')
    radius = request.GET.get('radius', 2000)  # Default radius = 2000m

    # Validate coordinates
    try:
        user_latitude = float(user_latitude)
        user_longitude = float(user_longitude)
        radius = float(radius)
    except (TypeError, ValueError):
        return Response({'error': 'Invalid latitude, longitude, or radius.'}, status=status.HTTP_400_BAD_REQUEST)

    user_location = Point(user_longitude, user_latitude, srid=4326)

    # Query: Filter events within the radius & sort by distance
    nearby_events = Event.objects.annotate(
        distance=Distance('location__coordinates', user_location)
    ).filter(distance__lte=radius).order_by('distance')

    serializer = EventSerializer(nearby_events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# --------------------------- EVENT MANAGEMENT ---------------------------

@swagger_auto_schema(
    method='post',
    operation_description="Create a new event",
    request_body=EventSerializer,
    responses={201: EventSerializer, 400: "Bad Request"},
)
@api_view(['POST'])
def create_event(request):
    """
    Create a new event.
    """
    serializer = EventSerializer(data=request.data)

    if serializer.is_valid():
        event = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='PUT',
    operation_description="Update an existing event",
    request_body=EventSerializer,
    responses={200: EventSerializer, 404: "Not Found", 400: "Bad Request"},
)
@api_view(['PUT'])
def update_event(request, pk):
    """
    Update an existing event by ID.
    """
    event = get_object_or_404(Event, pk=pk)
    serializer = EventSerializer(event, data=request.data)

    if serializer.is_valid():
        event = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete an event",
    responses={204: "No Content", 404: "Not Found"},
)
@api_view(['DELETE'])
def delete_event(request, pk):
    """
    Delete an event by ID.
    """
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------- ACTIVITY MANAGEMENT ---------------------------

@swagger_auto_schema(
    method='GET',
    responses={200: ActivitiesSerializer(many=True), 400: "Bad request"},
)
@api_view(['GET'])
def list_nearby_activities(request):
    """
    Lists nearby activities **sorted by distance** from the user's location.
    """
    user_latitude = request.GET.get('lat')
    user_longitude = request.GET.get('lon')
    radius = request.GET.get('radius', 2000)  # Default radius = 2000m

    # Validate coordinates
    try:
        user_latitude = float(user_latitude)
        user_longitude = float(user_longitude)
        radius = float(radius)
    except (TypeError, ValueError):
        return Response({'error': 'Invalid latitude, longitude, or radius.'}, status=status.HTTP_400_BAD_REQUEST)

    user_location = Point(user_longitude, user_latitude, srid=4326)

    # Query: Filter activities within the radius & sort by distance
    nearby_activities = Activity.objects.annotate(
        distance=Distance('location__coordinates', user_location)
    ).filter(distance__lte=radius).order_by('distance')

    serializer = ActivitiesSerializer(nearby_activities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    request_body=ActivitiesSerializer,
    responses={201: ActivitiesSerializer, 400: "Bad Request"},
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


@swagger_auto_schema(
    method='PUT',
    operation_description="Update an existing activity",
    request_body=ActivitiesSerializer,
    responses={200: ActivitiesSerializer, 404: "Not Found", 400: "Bad Request"},
)
@api_view(['PUT'])
def update_activity(request, pk):
    """
    Update an existing activity by ID.
    """
    activity = get_object_or_404(Activity, pk=pk)
    serializer = ActivitiesSerializer(activity, data=request.data)

    if serializer.is_valid():
        activity = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete an activity",
    responses={204: "No Content", 404: "Not Found"},
)
@api_view(['DELETE'])
def delete_activity(request, pk):
    """
    Delete an activity by ID.
    """
    activity = get_object_or_404(Activity, pk=pk)
    activity.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------- FOOD MANAGEMENT ---------------------------

@swagger_auto_schema(
    method='post',
    operation_description="Create a new food item",
    request_body=FoodSerializer,
    responses={201: FoodSerializer, 400: "Bad Request"},
)
@api_view(['POST'])
def create_food(request):
    """
    Create a new food item.
    """
    serializer = FoodSerializer(data=request.data)

    if serializer.is_valid():
        food = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={200: FoodSerializer(many=True), 404: "Not Found"},
)
@api_view(['GET'])
def list_food(request):
    """
    List all food items.
    """
    food_items = Food.objects.all()
    serializer = FoodSerializer(food_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='put',
    operation_description="Update a food item",
    request_body=FoodSerializer,
    responses={200: FoodSerializer, 404: "Not Found", 400: "Bad Request"},
)
@api_view(['PUT'])
def update_food(request, pk):
    """
    Update a specific food item by ID.
    """
    food_item = get_object_or_404(Food, pk=pk)
    serializer = FoodSerializer(food_item, data=request.data)

    if serializer.is_valid():
        food = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='DELETE',
    operation_description="Delete a food item",
    responses={204: "No Content", 404: "Not Found"},
)
@api_view(['DELETE'])
def delete_food(request, pk):
    """
    Delete a specific food item by ID.
    """
    food_item = get_object_or_404(Food, pk=pk)
    food_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
