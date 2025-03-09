from django.db.models.signals import post_save, post_delete  
from django.dispatch import receiver  
from django.conf import settings  
from .models import Profile

# Signal to automatically create a profile when a new user is registered
@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # This function runs when a User instance is saved
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile instance whenever a new User is created.
    
    Parameters:
    - sender: The model that sends the signal (User model in this case).
    - instance: The actual instance of the model being saved.
    - created: Boolean, True if a new user was created, False if updated.
    - kwargs: Additional keyword arguments.
    """
    if created:  # Only execute if a new user is created (not when an existing user is updated)
        Profile.objects.create(user=instance)  # Create a Profile linked to the user

# Signal to save the profile whenever the user instance is updated
@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # Runs after a User instance is saved
def save_user_profile(sender, instance, **kwargs):
    """
    Saves the associated Profile instance whenever the User instance is saved.
    
    Ensures any updates to the User model (e.g., username, email) are reflected in the Profile model.
    
    Parameters:
    - sender: The model that sends the signal (User model).
    - instance: The actual User instance being saved.
    - kwargs: Additional keyword arguments.
    """
    instance.profile.save()  # Save the profile associated with the user instance


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_user_profile(sender, instance, **kwargs):
    """
    Deletes the associated Profile instance whenever the User instance is deleted.
    """
    try:
        instance.profile.delete()  # Delete the associated profile
    except Profile.DoesNotExist:
        print("Profile does not exist")

@receiver(post_save, sender=Profile)
def sync_profile(sender, instance, **kwargs):
    """Sync profile updates to all databases when the profile is saved."""
    databases = ['subsidiary_1', 'subsidiary_2']

    for db in databases:
        Profile.objects.using(db).update_or_create(
            user=instance.user,
            defaults={"bio": instance.bio, "phone_number": instance.phone_number}
        )