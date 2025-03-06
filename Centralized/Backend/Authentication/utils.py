from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse

def generate_verification_link(user):
    """
    Generates an email verification link for a new user.
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))  # Encode the user's ID
    token = default_token_generator.make_token(user)  # Generate a secure token
    verification_url = reverse("verify-email", kwargs={"uidb64": uid, "token": token})  # Generate the URL
    full_url = f"http://127.0.0.1:8000{verification_url}"  # Modify with actual frontend domain

    return full_url

def send_verification_email(user):
    """
    Sends a verification email with an activation link.
    """
    verification_link = generate_verification_link(user)
    subject = "Verify Your Email"
    message = f"Click the link below to verify your email and activate your account:\n\n{verification_link}"
    
    send_mail(
        subject,
        message,
        "aryan223653badkul@gmail.com",  # Sender email
        [user.email],  # Recipient email
        fail_silently=False,
    )
