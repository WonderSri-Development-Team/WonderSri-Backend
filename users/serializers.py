from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'last_name', 'first_name']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    def validate_email(self, value):
        """
        Ensure the email is unique (case insensitive).
        """
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        """
        Ensure the username is unique (case insensitive).
        """
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_password(self, value):
        """
        Validate the password to ensure it meets certain complexity requirements.
        """
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return value

    def create(self, validated_data):
        """
        Override the default create method to hash the password using `create_user`.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']  # Automatically hashes the password
        )
        return user

from .models import UserProfile, UserVisit, SavedItem

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'preferred_language', 'notification_radius', 'interests', 'email_verified', 'profile_picture']
        
class UserVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVisit
        fields = ['id', 'location', 'visited_at', 'rating', 'comment']
        
class SavedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedItem
        fields = ['id', 'item_type', 'item_id', 'saved_at', 'notes']
    
