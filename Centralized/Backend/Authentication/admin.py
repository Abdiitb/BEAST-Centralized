from django.contrib import admin  # Import Django admin module
from django.contrib.auth import get_user_model  # Get the custom User model
from .models import Profile

# Retrieve the User model defined in AUTH_USER_MODEL (settings.py)
User = get_user_model()

# Register the User model in Django Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Define which fields will be displayed in the admin panel
    list_display = ["id", "username", "email", "is_active", "is_staff"]

admin.site.register(Profile)
