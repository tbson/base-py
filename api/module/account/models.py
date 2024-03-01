import os
import uuid
from typing import Any, Optional

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from module.account.const import PROFILE_TYPE_CHOICE, PROFILE_TYPE_DICT, ProfileType
from type.schema import PemSchema, RoleSchema, TenantSchema, UserSchema
from util.framework.model.timestamped_model import TimestampedModel


def upload_to(instance: models.ImageField, filename: str) -> str:
    ext = filename.split(".")[-1]
    return os.path.join("avatar", f"{uuid.uuid4()}.{ext}")


class Tenant(TimestampedModel, TenantSchema):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = "tenants"
        ordering = ["-id"]


class Pem(models.Model, PemSchema):
    title = models.CharField(max_length=128)
    module = models.CharField(max_length=128)
    action = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = "pems"
        unique_together = ["module", "action"]
        ordering = ["-id"]


class Role(TimestampedModel, RoleSchema):
    tenant = models.ForeignKey(
        Tenant,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        related_name="roles",
        verbose_name=_("tenant"),
    )
    profile_type = models.IntegerField(
        choices=PROFILE_TYPE_CHOICE, default=ProfileType.USER
    )
    pems = models.ManyToManyField(Pem, blank=True, related_name="roles")
    title = models.CharField(max_length=128)
    default = models.BooleanField(default=False)

    @property
    def pem_ids(self) -> list[int]:
        return list(self.pems.values_list("id", flat=True))

    @property
    def profile_type_label(self) -> str:
        return PROFILE_TYPE_DICT.get(self.profile_type, "Unknown")

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = "roles"
        unique_together = ["tenant", "title"]
        ordering = ["-id"]


class User(AbstractUser, UserSchema):
    tenant = models.ForeignKey(
        Tenant,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name=_("tenant"),
    )
    roles = models.ManyToManyField(Role, blank=True, related_name="users")
    email = models.EmailField(max_length=128, unique=True)
    mobile = models.CharField(
        max_length=16, unique=True, null=True, blank=True, default=None
    )
    avatar = models.ImageField(upload_to=upload_to, blank=True, null=True)
    info = models.JSONField(default=dict, blank=True)
    refresh_token_signature = models.CharField(max_length=128, blank=True, default="")
    email_verified = models.DateTimeField(null=True, default=None)
    mobile_verified = models.DateTimeField(null=True, default=None)
    last_change_pwd = models.DateTimeField(null=True, default=None)
    last_reset_pwd = models.DateTimeField(null=True, default=None)

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}".strip()

    @property
    def role_ids(self) -> list[int]:
        return list(self.roles.values_list("id", flat=True))

    def __str__(self) -> str:
        return self.email

    def clean(self) -> None:
        self.username = self.email

    def save(self, *args: Optional[Any], **kwargs: Optional[Any]) -> None:
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "users"
        ordering = ["-id"]
        verbose_name = _("user")
