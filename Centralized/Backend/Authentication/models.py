from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
import uuid
from .options import HOSTEL_CHOICES
from django.db import connections

# Custom User Manager for handling user creation
class UserManager(BaseUserManager):
    """
    Custom manager for User model where ldap is the unique identifier.
    This handles both regular user and superuser creation.
    """

    def create_user(self, username, ldap, password=None, **extra_fields):
        """
        Creates and returns a regular user with the given ldap and password.
        """
        if not ldap:
            raise ValueError("LDAP is required")  # Ensure LDAP is provided

        ldap = self.normalize_email(ldap)  # Standardize email format
        user = self.model(username=username, ldap=ldap, **extra_fields)  # Create a new user instance
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)  # Save user in the database
        return user

    def create_superuser(self, username, ldap, password, **extra_fields):
        """
        Creates and returns a superuser with admin privileges.
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)  # Superuser can access Django admin
        extra_fields.setdefault("is_superuser", True)  # Superuser has all permissions

        return self.create_user(username, ldap, password, **extra_fields)


# Custom User Model extending AbstractBaseUser and PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model replacing Django's default User model.
    Uses email instead of username for authentication.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True) # Unique ID for the user
    ldap = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=150, unique=True)  # Unique username
    email = models.EmailField(max_length=100)  # Unique email for authentication
    # full_name = models.CharField(max_length=255)  # User's full name
    roll_number = models.CharField(max_length=20, unique=True)  # Unique roll number
    hostel_number = models.CharField(choices=HOSTEL_CHOICES)  # Hostel number of the user

    is_active = models.BooleanField(default=False)  # Determines if user can log in
    is_staff = models.BooleanField(default=False)  # Grants admin panel access if True
    is_verified = models.BooleanField(default=False)

    objects = UserManager()  # Assigning UserManager to handle user creation

    USERNAME_FIELD = "ldap"  # Login authentication field
    REQUIRED_FIELDS = ["username", "email", "roll_number", "hostel_number"]  # Mandatory fields when creating a user

    def __str__(self):
        """
        Returns the string representation of the user model (email).
        """
        return self.username
    
class Profile(models.Model):
    """
    Profile model to store additional user information.
    Linked to the User model via a OneToOneField.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, null=True)  # Short bio of the user
    # profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)  # User's profile picture
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number

    def save(self, *args, **kwargs):
        """Save to all databases when a profile is updated."""
        super().save(*args, **kwargs)  # Save to the default (centralized) database

        # Synchronize changes to subsidiary databases
        for db in ['ilp']:
            with connections[db].cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Authentication_profile (user_id, bio, phone_number)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE
                    SET bio = EXCLUDED.bio, phone_number = EXCLUDED.phone_number
                    """,
                    [self.user_id, self.bio, self.phone_number]
                )

    def __str__(self):
        """
        Returns the username of the associated user.
        """
        return f"{self.user.username}'s Profile"