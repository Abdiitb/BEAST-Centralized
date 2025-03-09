from django.contrib import admin
from .models import Registration, WishList
# from .views import export_csv, export_csv_wishlist, export_registrations_to_csv
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Define resource class
class UserResource_Reg(resources.ModelResource):
    class Meta:
        model = Registration  # Replace with your model


class UserResource_Wish(resources.ModelResource):
    class Meta:
        model = WishList  # Replace with your model

@admin.register(Registration)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource_Reg

@admin.register(WishList)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource_Wish
# Register your models here.
# def export_selected_to_csv(modeladmin, request, queryset):
#     return export_csv(request)

# export_registrations_to_csv.short_description = "Export selected selected to CSV"

# class RegistrationAdmin(admin.ModelAdmin):
#     actions = [export_registrations_to_csv]

# admin.site.register(Registration)

# def export_selected_to_csv_wishlist(modeladmin, request, queryset):
#     return export_csv_wishlist(request, queryset)

# export_selected_to_csv_wishlist.short_description = "Export selected wishlist to CSV"

# class WishListAdmin(admin.ModelAdmin):
#     actions = [export_selected_to_csv_wishlist]

# admin.site.register(WishList)