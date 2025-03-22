from django.utils.http import urlsafe_base64_decode
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import ValidationError
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
from .models import UserProfile
from .utils import send_reset_email, send_email_verification_email
from .serializers import UserSerializer, ProfileSerializer, ProfilePictureSerializer
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str


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

        # Check if the password is correct first
        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Ensure email is verified (assuming you have an is_verified field)
        if not user.is_active:  # Adjust this if you're using a different field
            return Response({'error': 'Please verify your email before logging in.'}, status=status.HTTP_403_FORBIDDEN)

    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)  # Prevent user enumeration

    # ✅ Generate JWT tokens ONLY after all checks pass
    refresh = RefreshToken.for_user(user)
    serializer = UserSerializer(instance=user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': serializer.data
    }, status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='post',
    operation_description="Signup new user and return JWT tokens",
    request_body=UserSerializer,
    responses={
        201: openapi.Response(description="User registered successfully", schema=auth_response_schema),
        400: "Bad Request (Invalid data or user already exists)"
    }
)
@api_view(['POST'])
def signup(request):
    """Signup new user and return JWT tokens."""
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'A user with this username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        user.is_active = False
        user.save()

        UserProfile.objects.create(user=user)

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        send_email_verification_email(user)

        return Response({
            'refresh': str(refresh),
            'access': access,
            'user': serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
    responses={
        200: "Email verification successful",
        400: "Invalid token",
    }
)
@api_view(['GET'])
def verify_email(request, uidb64, token):
    """
    View to handle email verification links.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Token is valid, activate the user
        user.is_active = True
        user.save()
        # You can redirect to a success page here
        return Response({'message': 'Email verification successful'}, status=status.HTTP_200_OK)
    else:
        # Invalid token or user
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

"""
USER MANAGEMENT 
"""

@swagger_auto_schema(
    method='post',
    operation_description="Change username",
    request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description="New username")
    },
    required=['username'],
)
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_username(request):
    username = request.data.get('username')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)

    user.username = username
    user.save()
    return Response({'message': 'Username changed successfully.'}, status=status.HTTP_200_OK)

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
def reset_password(request, uidb64, token):
    """Reset user password using the provided token."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

    if user and default_token_generator.check_token(user, token):
        new_password = request.data.get('password')

        # Validate password (Ensure it's not empty)
        if not new_password:
            return Response({'error': 'Password is missing'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
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
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Allow logged-in users to change their password."""
    user = request.user

    old_password = request.data.get('old_password')
    confirm_password = request.data.get('confirm-password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({'error': 'Old password and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

    if confirm_password != new_password:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(old_password):
        return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    operation_description="Change email for logged-in user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="New email"),},
        required=['email'],
    ),
    responses={
        200: "Email changed successfully",
        400: "Bad Request (Email missing)",
        409: "Email already registered",
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_email(request):
    email = request.data.get('email')

    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_409_CONFLICT)

        # Validate email format
        user = request.user
        user.email = email
        user.full_clean()
        user.save()

    except ValidationError:
        return Response({'error': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Email changed successfully'}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='delete',
    operation_description="Delete account for logged-in user",
    responses={
        204: "Account deleted successfully",
        401: "Unauthorized",
    }
)
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_account(request):
    try:
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': 'Failed to delete account.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    operation_description="Getting account details for logged-in user",
    responses={
        200: "Information read!",
        401: "Unauthorized",
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_account(request):
    user = request.user

    return Response({'username': user.username, 'email': user.email}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='put',
    operation_description="Allows users to upload or update their profile picture.",
    request_body=ProfileSerializer,
    responses={
        200: ProfileSerializer,
        400: "Bad Request"
    }
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Allows users to update their profile attributes including profile picture, phone number, gender and  date of birth.
    """
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    serializer = ProfileSerializer(user_profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Profile updated successfully!",
            "profile": serializer.data
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='GET',
    operation_description="Retrieve the user's profile data.",
    responses={
        200: ProfileSerializer,
        401: "Unauthorized"
    }
)
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """Retrieve the user's profile data."""
    user_profile = UserProfile.objects.get(user=request.user)
    serializer = ProfileSerializer(user_profile)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    operation_description="Upload Profile Picture",
    responses={
        200: ProfilePictureSerializer,
        401: "Unauthorized"
    }
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_profile_picture(request):
    """
    Allows users to upload or update their profile picture.
    """
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    serializer = ProfilePictureSerializer(user_profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Profile picture updated successfully!",
            "profile_picture_url": user_profile.profile_picture.url  # Return the URL of the uploaded image
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


