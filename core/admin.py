from django.contrib import admin

from account.models import Student, Staff
from .models import Department,User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name","department_code","description","created_at")
    list_per_page = 10


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("first_name","last_name","email","last_login")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "username")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "role", "username","password"),
            },
        ),
    )
    search_fields = ("username", "email","first_name", "last_name")
    ordering = ("created_at",)





