from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_active")
    search_fields = ("email",)
    ordering = ("email",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
