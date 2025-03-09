from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import IsAuthenticated
from .models import Profile

User = get_user_model()
#
class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        ldap = request.data.get('ldap')
        password = request.data.get('password')
        user = authenticate(username=ldap, password=password)

        if user.is_active and user.is_verified:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        
        elif not user.is_active and not user.is_verified:
            return Response({"error": "User not verified, please verify your account from your webmail"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class VerifyEmailView(APIView):
    """
    View to handle email verification using a token.
    """

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))  # Decode the user ID
            user = get_object_or_404(User, pk=uid)  # Retrieve the user
            
            if default_token_generator.check_token(user, token):  # Validate the token
                user.is_verified = True
                user.is_active = True  # Allow user to log in after verification
                user.save()
                return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    """
    API View to retrieve the authenticated user's profile.
    """
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def get(self, request):
        """
        Handle GET request to fetch user profile details, including associated User data.
        """
        profile = get_object_or_404(Profile.objects.select_related("user"), user=request.user)
        serializer = ProfileSerializer(profile)  # Serialize profile and nested user data
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request):
        """
        Handle PUT request to update user profile details.
        """
        try:
            profile = request.user.profile  # Get the logged-in user's profile
            serializer = ProfileSerializer(profile, data=request.data, partial=True)  # Serialize with new data

            if serializer.is_valid():
                serializer.save()  # Save the updated profile data
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Profile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)