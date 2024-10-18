from django.contrib import admin
from schedule_manager.models import (
    User,
    Schedule
)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """Custom User Admin."""

    list_display = ("email", "first_name", "last_name", "is_active", "is_superuser", "last_login", "last_logout_at")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "is_superuser")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields":
            (
                "first_name",
                "last_name",
            )
        }),
        ("Permissions", {"fields": ("is_active", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )
    ordering = ("-created_at",)
    filter_horizontal = ()


@admin.register(Schedule)
class CustomScheduleAdmin(admin.ModelAdmin):
    """Custom Schedule Admin."""

    list_display = ("id", "day", "start", "stop")
    search_fields = ("day",)
    list_filter = ("day",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields":
            (
                "day",
                "user",
                "start",
                "stop",
                "badge_ids",
                "camera_ids"
            )
        }),
        ("Important dates", {"fields": ("created_at", "updated_at")}),
    )
    ordering = ("-created_at",)
    filter_horizontal = ()
