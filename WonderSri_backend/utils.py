from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings

def generate_password_reset_link(user):
    """
    Generate a password reset link for the given user using SimpleJWT tokens.
    """
    refresh = RefreshToken.for_user(user)
    reset_link = f"http://127.0.0.1:8000/reset-password/{user.id}/{refresh}/"
    return reset_link


def send_reset_email(user, reset_link):
    """
    Send a password reset email to the user.
    """
    email_subject = "Password Reset Request - WonderSri"
    email_message = (
        f"Hello {user.username},\n\n"
        "We received a request to reset your password. Please click the link below to reset it:\n\n"
        f"{reset_link}\n\n"
        "If you did not request a password reset, please ignore this email.\n\n"
        "Best regards,\nThe WonderSri Team"
    )
    send_mail(
        email_subject,
        email_message,
        settings.EMAIL_HOST_USER,  # Configurable sender email
        [user.email],
    )
