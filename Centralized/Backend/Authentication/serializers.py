from rest_framework import serializers  # Importing Django REST framework's serializer module
from django.contrib.auth import get_user_model  # Importing the custom user model
from .models import Profile

# Getting the custom User model (useful when using a custom User model instead of Django's default User)
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles user creation and ensures password is write-only.
    """

    password = serializers.CharField(write_only=True)  # Prevents password from being exposed in responses

    class Meta:
        model = User  # Specifies the model to be serialized
        fields = ["id", "ldap", "username", "email", "roll_number", "hostel_number", "password"]  # Fields to include in serialization

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        
        from .utils import send_verification_email  # Import the email function
        send_verification_email(user)  # Send the email verification link

        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()
    class Meta:
        model = Profile
        fields = "__all__"
