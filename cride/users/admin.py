""" User models admin """

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from cride.users.models import User, Profile


class CustomeUserAdmin(UserAdmin):
    """User model admin. """
    list_display = ("email", "username", "first_name", "last_name", "is_staff", "is_client", "is_verified")
    list_filter = ("is_client", "is_staff", "created", "modified")


admin.site.register(User, CustomeUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ Profile model admin. """
    list_display = ("user", "reputation", "rides_taken", "rides_offered")
    list_search = ("user__username", "user__email", "user__first_name", "user__last_name")
    list_filter = ("reputation",)
