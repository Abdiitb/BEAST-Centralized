from django.contrib import admin
from .models import Project
# from .views import export_projects_to_csv
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Define resource class
class UserResource(resources.ModelResource):
    class Meta:
        model = Project  # Replace with your model

# export_projects_to_csv.short_description = "Export selected projects to CSV"

@admin.register(Project)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource