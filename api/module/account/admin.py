from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Tenant, User


class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "validate",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("mobile", "email")


class CustomUserChangeForm(UserChangeForm):
    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "validate",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("mobile", "email")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "is_staff", "is_superuser")
    list_filter = ("email", "is_staff", "is_superuser")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "mobile", "first_name", "last_name", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "mobile",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("id", "uid", "title")
