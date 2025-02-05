import jwt
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
from WonderSri_backend import settings
from .utils import send_reset_email, send_email_verification_email
from .serializers import UserSerializer
from google.oauth2 import id_token
from google.auth.transport import requests

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
    """Login user and return JWT tokens only if email is verified."""
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)

        # Check if the email is verified
        if not user.is_active:
            return Response({'error': 'Please verify your email before logging in.'}, status=status.HTTP_403_FORBIDDEN)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    # Generate JWT tokens
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
        user.is_active = False  #Prevents log in without verifying
        user.save()

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        send_email_verification_email(user)

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


    send_reset_email(user)

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
    method='post',
    operation_description="Logout the user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token")},
        required=['refresh_token'],
    ),
    reponses={'200': "Logout successful",'400': "Bad Request"}
)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


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

@swagger_auto_schema(
    method='post',
    operation_description="Google OAuth login using ID token",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id_token': openapi.Schema(type=openapi.TYPE_STRING, description="Google ID token")},
        required=['id_token'],
    ),
    responses={
        '200': openapi.Response(description="Google OAuth login successful"),
        '400': openapi.Response(description="Bad Request")
    }
)
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def googleoauthlogin(request):
    id_token_data = request.data.get('id_token')  # Use ID token, not refresh token

    if not id_token_data:
        return Response({'error': 'ID Token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Replace 'YOUR_GOOGLE_CLIENT_ID' with your actual Google OAuth client ID
        CLIENT_ID = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY

        # Verify the Google ID token
        id_info = id_token.verify_oauth2_token(id_token_data, requests.Request(), CLIENT_ID)

        # Ensure the token is intended for your app
        if id_info['aud'] != CLIENT_ID:
            raise ValueError('Invalid audience')

        # Find or create user based on Google email
        user, created = User.objects.get_or_create(
            email=id_info['email'],
            defaults={'username': id_info['email']}
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({'error': 'Invalid token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_description="Verify email",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING, description="Token")},
        required=['token'],
    )
)
@api_view(['GET'])
def verify_email(request, token):
    """Verify email using the token sent via email."""
    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])

        if user.is_active:
            return Response({'message': 'Email already verified.'}, status=status.HTTP_200_OK)

        # Activate the user
        user.is_active = True
        user.save()

        return Response({'message': 'Email verified successfully! You can now log in.'}, status=status.HTTP_200_OK)

    except jwt.ExpiredSignatureError:
        return Response({'error': 'Verification link expired. Please request a new one.'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.DecodeError:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

