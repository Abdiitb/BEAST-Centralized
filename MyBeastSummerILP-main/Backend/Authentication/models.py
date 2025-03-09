import uuid
from django.db import models
from Projects.options import HOSTEL_CHOICES 
import requests
# class User(models.Model):
#     fullname = models.CharField(max_length=100)
#     ldap = models.EmailField(max_length=100, unique=True)
#     dept = models.CharField(max_length=100)
#     degree = models.CharField(max_length=100)
#     program = models.CharField(max_length=100)
#     contact = models.CharField(max_length=10)
#     password = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=False)
#     accessToken = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

#     def __str__(self):
#         return self.fullname + " " + self.ldap

#     def save(self, *args, **kwargs):
#         if not self.accessToken: 
#             self.accessToken = uuid.uuid4()
#         super(User, self).save(*args, **kwargs) 

# class Token(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     token = models.UUIDField(default=uuid.uuid4, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.fullname + " " + str(self.token)

class Profile(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) # Unique ID for the user
    ldap = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=150, unique=True)  # Unique username
    email = models.EmailField(max_length=100)  # Unique email for authentication
    # full_name = models.CharField(max_length=255)  # User's full name
    roll_number = models.CharField(max_length=20, unique=True)  # Unique roll number
    hostel_number = models.CharField(choices=HOSTEL_CHOICES)  # Hostel number of the user
    # personal_email = models.EmailField(max_length=200)
    linkedin = models.CharField(max_length=200, blank=True, null=True)
    resume_link = models.CharField(max_length=500, blank=True, null=True)
    asc_ss_link = models.CharField(max_length=500, blank=True, null=True)
    projects = models.CharField(max_length=5000, blank=True, null=True)
    internships = models.CharField(max_length=5000, blank=True, null=True)
    pors = models.CharField(max_length=5000, blank=True, null=True)

    # Subsidiary has additional fields, but we only sync common ones
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save profile first

        # Send update to subsidiary website
        try:
            data = {
                "user_id": str(self.user_id),
                "username": self.username,
                "email": self.email,
                "roll_number": self.roll_number,
                "hostel_number": self.hostel_number
            }
            requests.post("http://127.0.0.1:8000/api/authentication/profile_update/", json=data)
        except Exception as e:
            print("Error sending update to subsidiary:", e)

    def __str__(self):
        return self.username + " " + self.ldap