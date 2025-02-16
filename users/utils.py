from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_reset_email(user):
    """
    Send a password reset email to the user.
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"https://wondersri-backend.onrender.com/auth/reset-password/{uid}/{token}/"

    email_subject = "WonderSri - Reset Your Password"
    subject = "Reset your password"
    from_email = "WonderSri <wondersriteam@gmail.com>"
    to_email = user.email

    # Render the HTML template with context
    html_message = render_to_string('password_reset_email.html', {
        'user': user,
        'verification_link': reset_link
    })

    # Create the email
    email = EmailMultiAlternatives(subject, '', from_email, [to_email])
    email.attach_alternative(html_message, "text/html")

    # Send the email
    email.send()

def send_email_verification_email(user):
    """
    Send an email verification link to the user.
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = f"https://wondersri-backend.onrender.com/auth/verify-email/{uid}/{token}/"

    email_subject = "WonderSri Verification"
    subject = "Verify Your Email Address"
    from_email = "WonderSri <wondersriteam@gmail.com>"
    to_email = user.email

    # Render the HTML template with context
    html_message = render_to_string('email_verification_mail.html', {
        'user': user,
        'verification_link': verification_link
    })

    # Create the email
    email = EmailMultiAlternatives(subject, '', from_email, [to_email])
    email.attach_alternative(html_message, "text/html")

    # Send the email
    email.send()

