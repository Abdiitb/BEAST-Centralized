from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer
from .models import Profile
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.shortcuts import rProfiler
import requests
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
from django.shortcuts import get_object_or_404
from django.conf import settings
# import smtplib
# import os

# class CreateUserAPIView(APIView):
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
            
#             token, created = Token.objects.get_or_create(user=user)
            
#             print("User created successfully")
#             print("Token: ", token)
            
#             send_sso_mail(emailid=user.ldap, token=token.token)
            
#             response_data = serializer.data.copy()
#             response_data.pop('password', None)
#             response_data.pop('accessToken', None)
            
#             return Response(response_data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TokenVerification(APIView):
#     def post(self, request, format=None):
#         try:
#             token = Token.objects.get(token=request.data['token'])
#             user = token.user
#             if(user.is_active):
#                 return Response("User already verified",status=status.HTTP_400_BAD_REQUEST)
#             user.is_active = True
#             user.save()
#             return Response("Verificaiton Successful",status=status.HTTP_200_OK)
#         except Exception as e:
#             print("Error while verifying token", e)
#             return Response("No user found, please signup",status=status.HTTP_400_BAD_REQUEST)

CENTRAL_AUTH_URL = f"{settings.CENTRAL_API_BASE}/api/authentication/profile/"
CENTRAL_TOKEN_URL = f"{settings.CENTRAL_API_BASE}/api/authentication/login/"

print('CENTRAL_AUTH_URL :', CENTRAL_AUTH_URL)
print('CENTRAL_TOKEN_URL :', CENTRAL_TOKEN_URL)

def fetch_user_from_api(url,token):
        """Fetch user details from the centralized authentication system."""
        headers = {"Authorization": token}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()  # Return user data from the central system
        return None

class LoginView(APIView):
    def post(self, request):
        """Authenticate the user via the centralized system and return a JWT token."""

        # Debugging: Print request body received by Django
        # print("Received Request Body:", request.body)  # Raw data
        # print("Received Request Data:", request.data)  # Parsed data

        ldap = request.data.get("ldap")
        password = request.data.get("password")

        if not ldap or not password:
            return Response({"error": "LDAP and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Send login request to the centralized authentication system
        response = requests.post(CENTRAL_TOKEN_URL, data={"ldap": ldap, "password": password})

        print("Central API Response:", response.text)  # Debugging response

        if response.status_code == 200:
            accessToken = response.json().get("access")  # Assuming the response contains an access token
            refreshToken = response.json().get("refresh")  # Assuming the response contains a refresh token

            user_profile_ilp = fetch_user_from_api(f"{settings.API_BASE_URL}/api/authentication/profile/", f"Bearer {accessToken}")

            # print("ILP API Response:", user_profile_ilp)

            if not user_profile_ilp:
                user_profile_centralized = fetch_user_from_api(CENTRAL_AUTH_URL, f"Bearer {accessToken}")

                # print("Central API Response:", user_profile_centralized)

                response_profile = requests.post(f'{settings.API_BASE_URL}/api/authentication/profile/', headers={"Authorization": f"Bearer {accessToken}"})

                # print("ILP API Response for Profile:", response_profile)
            return Response({"accessToken": accessToken, "refreshToken": refreshToken}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class ProfileView(APIView):

    def get(self, request):
        """Retrieve the profile details of the authenticated user."""
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        user_data = fetch_user_from_api(CENTRAL_AUTH_URL, token)
        # print('user_data :', user_data)
        if not user_data:
            return Response({"error": "Invalid token or user not found"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = user_data.get("user").get("id")
        profile = get_object_or_404(Profile, user_id=user_id)
        serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new profile or update an existing one based on centralized authentication."""
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        user_data = fetch_user_from_api(CENTRAL_AUTH_URL, token)  # Assuming the data is sent in the request body   
        if not user_data:
            return Response({"error": "Invalid token or user not found"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = user_data.get("user").get("id")
        ldap = user_data.get("user").get("ldap")
        username = user_data.get("user").get("username")
        email = user_data.get("user").get("email")
        roll_number = user_data.get("user").get("roll_number")
        hostel_number = user_data.get("user").get("hostel_number")
        # linkedin = user_data.get("user").get("linkedin")
        # resume_link = user_data.get("user").get("resume_link")
        # asc_ss_link = user_data.get("user").get("asc_ss_link")
        # projects = user_data.get("user").get("projects")
        # internships = user_data.get("user").get("internships")
        # pors = user_data.get("user").get("pors")


        profile, created = Profile.objects.update_or_create(
            user_id=user_id,
            defaults={
                "ldap": ldap,
                "username": username, 
                "email": email,
                "roll_number": roll_number,
                "hostel_number": hostel_number,
                # "linkedin": linkedin,
                # "resume_link": resume_link,
                # "asc_ss_link": asc_ss_link,
                # "projects": projects,
                # "internships": internships,
                # "pors": pors
            }
        )

        serializer = ProfileSerializer(profile)
        return Response(
            {"message": "Profile created" if created else "Profile updated", "data": serializer.data},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    def put(self, request):
        """Update the profile details."""
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        user_data = fetch_user_from_api(f'{settings.API_BASE_URL}/api/authentication/profile/', token)
        if not user_data:
            return Response({"error": "Invalid token or user not found"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = user_data.get("id")
        print('user_id :', user_id)
        profile = get_object_or_404(Profile, id=user_id)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated", "data": serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete the profile."""
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        user_data = fetch_user_from_api(CENTRAL_AUTH_URL, token)
        if not user_data:
            return Response({"error": "Invalid token or user not found"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = user_data.get("id")
        profile = get_object_or_404(Profile, user_id=user_id)
        profile.delete()

        return Response({"message": "Profile deleted"}, status=status.HTTP_204_NO_CONTENT)

# def send_sso_mail(
#     mail_subject="User Verification of ILP 2023 | SARC IIT Bombay",
#     text_content="Yo man!",
#     emailid="akashbanger2@gmail.com",
#     token="",
#     name="Web CTM SARC",
#     sender_email="sarc@iitb.ac.in",
#     sender_name="SARC",
#     reply_name="SARC",
#     reply_to="nikhil@iitb.ac.in",
# ):
#     strFrom = "sarc@iitb.ac.in"
#     strTo = emailid
#     subject = mail_subject
#     text_content = text_content
#     token = token
#     msgRoot = MIMEMultipart("related")
#     msgRoot["Subject"] = mail_subject
#     msgRoot["From"] = strFrom
#     msgRoot["To"] = strTo
#     msgRoot.preamble = "This is a multi-part message in MIME format."
#     msgAlternative = MIMEMultipart("alternative")
#     msgRoot.attach(msgAlternative)
#     msghtml = f'''
# <!DOCTYPE html>
# <html>
#   <head>
#     <title>User Verification of ILP Summer 2024 | SARC IIT Bombay</title>
#   </head>
#   <body>
#     <div style="font-family: Arial, sans-serif; line-height: 1.5; background-color: #f8f8f8; margin: 0; padding: 0;">
#       <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #ffffff;">
#         <h1 style="font-size: 24px; color: #333333; margin-top: 0; margin-bottom: 20px;">User Verification of ILP Summer 2024 | SARC IIT Bombay</h1>
#         <p style="color: #555555; margin-bottom: 10px;">Dear User,</p>
#         <p style="color: #555555; margin-bottom: 10px;">
#           Thank you for signing up for the ILP. To complete your registration,
#           please click the following link to verify your email address:
#         </p>
#         <p style="margin-bottom: 10px;">
#           <a href="http://127.0.0.1:8000/verify-user/{token}" style="text-decoration: none; background-color: #007bff; color: #ffffff; padding: 10px 20px; border-radius: 5px;">Verify Email</a>
#         </p>
#       </div>
#     </div>
#   </body>
# </html>
# '''
    
    
    
#     msgText = MIMEText(
#         msghtml,
#         "html",
#     )

#     msgAlternative.attach(msgText)
#     smtp = smtplib.SMTP("smtp-auth.iitb.ac.in", 587)
#     smtp.starttls()
#     print(
#         "everything is fine till now--------------------------------------------------"
#     )
#     # smtp.login("210010007@iitb.ac.in", "")

#     try:
#       smtp.login("sarc@iitb.ac.in", "87638c40a92a794bc81b6de03e5ae86c")
#       response = smtp.sendmail(strFrom, strTo, msgRoot.as_string())
#       print("Response is ", response)
#       smtp.quit()
#       return response
#     except Exception as e:
#       print(e.message, "this is eeeeeeeeeeeeeeeeeee")
#       pass
  
  
# from django.http import HttpResponse
# import csv

# def export_users_to_csv(modeladmin, request, queryset):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="user_details.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['User ID', 'Full Name', 'LDAP', 'Department', 'Degree', 'Program', 'Contact', 'Personal Email', 'LinkedIn', 'Resume Link', 'ASC SS Link', 'Projects', 'Internships', 'PORs'])

#     queryset = queryset.order_by('id')

#     for user in queryset:
#         try:
#             profile = Profile.objects.get(user=user)
#         except:
#             profile = None
#         if(profile is not None):
#             writer.writerow([user.id, user.fullname, user.ldap, user.dept, user.degree, user.program, user.contact, profile.personal_email, profile.linkedin, profile.resume_link, profile.asc_ss_link, profile.projects, profile.internships, profile.pors])
#         else:
#             writer.writerow([user.id, user.fullname, user.ldap, user.dept, user.degree, user.program, user.contact])

#     return response
