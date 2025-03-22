from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError
import boto3
from django.conf import settings
import uuid


from users.models import UserProfile


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

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    username = serializers.CharField(source="user.username", required=False)
    email = serializers.EmailField(source="user.email", required=False)
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {
            'email': {'source': 'user.email', 'read_only': True},
            'first_name': {'source': 'user.first_name', 'read_only': True},
            'last_name': {'source': 'user.last_name', 'read_only': True},
            'username': {'source': 'user.username', 'read_only': True},
        }

    def update(self, instance, validated_data):
        # Update User model fields
        user_data = validated_data.pop("user", {})
        user = instance.user  # Access related user model

        if "first_name" in user_data:
            user.first_name = user_data["first_name"]
        if "last_name" in user_data:
            user.last_name = user_data["last_name"]
        if "email" in user_data:
            user.email = user_data["email"]
        if "username" in user_data:
            user.username = user_data["username"]

        user.save()

        return super().update(instance, validated_data)




class ProfilePictureSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    username = serializers.CharField(source='user.username', required=False)
    email = serializers.CharField(source='user.email', required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user

        # Update user details
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Handle Profile Picture Upload to S3
        profile_picture = validated_data.pop('profile_picture', None)
        if profile_picture:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            file_name = f"profile_pics/{profile_picture.name}"  # Unique filename

            # Upload file
            s3_client.upload_fileobj(
                profile_picture, bucket_name, file_name,
                ExtraArgs={'ContentType': profile_picture.content_type}  # Removed ACL
            )

            # Set the URL for profile_picture
            instance.profile_picture = f"https://{bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{file_name}"

        instance.save()  # Save UserProfile changes

        return instance


