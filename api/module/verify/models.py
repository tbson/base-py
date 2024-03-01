import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from module.verify.const import OTP_SOURCE_CHOICE, OTP_TYPE_CHOICE, OtpSource
from type.schema import OtpSchema, TrustedTargetSchema
from util.framework.model.timestamped_model import TimestampedModel


class Otp(TimestampedModel, OtpSchema):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target = models.CharField(max_length=128)
    type = models.IntegerField(choices=OTP_TYPE_CHOICE)
    source = models.IntegerField(choices=OTP_SOURCE_CHOICE, default=OtpSource.EMAIL)
    code = models.CharField(max_length=64)
    fail_checks = models.IntegerField(default=0)
    resend_expired_at = models.DateTimeField()
    ips = ArrayField(models.GenericIPAddressField(), default=list)
    verified_at = models.DateTimeField(null=True, default=None)
    expired_at = models.DateTimeField()
    extra_data = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return self.code

    class Meta:
        db_table = "otps"
        ordering = ["-id"]


class TrustedTarget(models.Model, TrustedTargetSchema):
    target = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.target

    class Meta:
        db_table = "trusted_targets"
        ordering = ["-id"]
