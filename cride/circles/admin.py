""" Circles. admin """

# Django
from django.contrib import admin

# Models
from cride.circles.models import Circle, Membership

admin.site.register(Membership)
@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display = (
        "name", 
        "slug_name",
        "is_public",
        "verified",
        "is_limited",
        "members_limit",
    )
    search_fields = ("slug_name", "name")
    list_filter = (
        "is_public",
        "verified",
        "is_limited",
    )