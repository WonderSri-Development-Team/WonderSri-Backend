from os import access

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.tokens import default_token_generator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .utils import generate_password_reset_link, send_reset_email
from .serializers import UserSerializer

# Ensure emails are unique
User._meta.get_field('email')._unique = True

# Reusable response schema for authentication responses
auth_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
        'access': openapi.Schema(type=openapi.TYPE_STRING),
        'user': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
    }
)


@swagger_auto_schema(
    method='post',
    operation_description="Login user and return JWT tokens",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="User email"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="User password"),
        },
        required=['email', 'password'],
    ),
    responses={
        200: openapi.Response(description="Login Successful", schema=auth_response_schema),
        400: "Bad Request (Missing credentials)",
        401: "Unauthorized (Invalid credentials)"
    }
)
@api_view(['POST'])
def login(request):
    """Login user and return JWT tokens."""
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


    refresh = RefreshToken.for_user(user)
    serializer = UserSerializer(instance=user)
    access = str(refresh.access_token)

    return Response({
        'refresh': str(refresh),
        'access': access,
        'user': serializer.data
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_description="Signup new user and return JWT tokens",
    request_body=UserSerializer,
    responses={
        201: openapi.Response(description="User registered successfully", schema=auth_response_schema),
        400: "Bad Request (Invalid data)"
    }
)
@api_view(['POST'])
def signup(request):
    """Signup new user and return JWT tokens."""
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({
            'refresh': str(refresh),
            'access': access,
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Request a password reset link via email",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'email': openapi.Schema(type=openapi.TYPE_STRING, description="User email")},
        required=['email'],
    ),
    responses={
        200: "Password reset link sent successfully",
        400: "Bad Request (Email required)",
        404: "User not found"
    }
)
@api_view(['POST'])
def request_password_reset(request):
    """Generate password reset link and send email."""
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    reset_link = generate_password_reset_link(user)
    send_reset_email(user, reset_link)

    return Response({'message': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_description="Reset password using token",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'password': openapi.Schema(type=openapi.TYPE_STRING, description="New password")},
        required=['password'],
    ),
    responses={
        200: "Password reset successful",
        400: "Bad Request (Invalid token or password missing)",
        404: "User not found"
    }
)
@api_view(['POST'])
def reset_password(request, user_id, token):
    """Reset user password using the provided token."""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not default_token_generator.check_token(user, token):
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

    new_password = request.data.get('password')
    if not new_password:
        return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    operation_description="Change password for logged-in user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'old_password': openapi.Schema(type=openapi.TYPE_STRING, description="Current password"),
            'new_password': openapi.Schema(type=openapi.TYPE_STRING, description="New password"),
        },
        required=['old_password', 'new_password'],
    ),
    responses={
        200: "Password updated successfully",
        400: "Bad Request (Incorrect old password or missing fields)"
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Allow logged-in users to change their password."""
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({'error': 'Old password and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(old_password):
        return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    operation_description="Test authentication endpoint",
    responses={200: "Authenticated successfully"}
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test_auth(request):
    """Test authentication endpoint."""
    return Response({'message': f'Authenticated as {request.user.username}'}, status=status.HTTP_200_OK)
