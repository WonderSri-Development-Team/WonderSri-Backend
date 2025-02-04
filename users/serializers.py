from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'last_name', 'first_name']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    def validate_password(self, value):
        """
        Validate the password to ensure it meets certain complexity requirements.
        """
        # Minimum length check
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        # Check for at least one digit
        if not re.search(r'\d', value):
            raise ValidationError("Password must contain at least one digit.")

        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least one uppercase letter.")

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', value):
            raise ValidationError("Password must contain at least one lowercase letter.")

        # Check for at least one special character
        if not re.search(r'[@$!%*?&]', value):
            raise ValidationError("Password must contain at least one special character.")

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
