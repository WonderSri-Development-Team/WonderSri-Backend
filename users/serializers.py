from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import boto3
from django.conf import settings
import uuid
from rest_framework import serializers
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
    class Meta:
        model = UserProfile
        fields = [ 'profile_picture','pic_url']

    def update(self, instance, validated_data):
        try:
            profile_picture = validated_data.pop('profile_picture', None)
            if profile_picture:
                try:
                    file_name = f"profile_pics/{uuid.uuid4().hex}_{profile_picture.name}"

                    try:
                        # Initialize S3 client
                        s3_client = boto3.client(
                            "s3",
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                            region_name=settings.AWS_REGION
                        )
                    except Exception as e:
                        raise serializers.ValidationError(f"Failed to initialize S3 client: {str(e)}")

                    try:
                        # Upload file to S3
                        s3_client.upload_fileobj(
                            profile_picture,
                            settings.AWS_STORAGE_BUCKET_NAME,
                            file_name,
                            ExtraArgs={'ContentType': profile_picture.content_type or 'application/octet-stream'}
                        )
                    except boto3.exceptions.S3UploadFailedError as e:
                        raise serializers.ValidationError(f"S3 upload failed: {str(e)}")
                    except boto3.exceptions.Boto3Error as e:
                        raise serializers.ValidationError(f"AWS error during upload: {str(e)}")
                    except Exception as e:
                        raise serializers.ValidationError(f"Unexpected error during file upload: {str(e)}")

                    try:
                        # Construct the full URL for the uploaded file
                        full_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{file_name}"

                        instance.pic_url = full_url
                    except Exception as e:
                        raise serializers.ValidationError(f"Failed to set profile picture attributes: {str(e)}")

                except Exception as e:
                    raise serializers.ValidationError(f"Error processing profile picture: {str(e)}")

            try:
                instance.save()
            except Exception as e:
                raise serializers.ValidationError(f"Failed to save profile: {str(e)}")

            return instance

        except serializers.ValidationError:
            raise
        except Exception as e:
            # Catch any other unexpected errors
            raise serializers.ValidationError(f"Unexpected error in profile picture update: {str(e)}")