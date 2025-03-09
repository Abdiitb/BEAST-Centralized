from django.contrib import admin
from .models import Blog
from import_export.admin import ImportExportModelAdmin  # ImportExport feature
from import_export import resources

# Define resource class
class UserResource(resources.ModelResource):
    class Meta:
        model = Blog  # Replace with your model

# Register model with ImportExport functionality
@admin.register(Blog)  # Replace with your model
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource