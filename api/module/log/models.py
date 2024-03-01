from django.contrib.postgres.fields import ArrayField
from django.db import models
from module.log.const import SECURITY_LOG_TYPE_CHOICE
from type.schema import AuditLogSchema, EmailLogSchema
from util.framework.model.timestamped_model import TimestampedModel


class EmailLog(TimestampedModel, EmailLogSchema):
    tenant_uid = models.UUIDField(null=True, default=None)
    to = ArrayField(models.EmailField(max_length=128), blank=False, null=False)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    server_response = models.TextField()

    def __str__(self) -> str:
        return self.subject

    class Meta:
        db_table = "email_logs"
        ordering = ["-id"]


class AuditLog(TimestampedModel, AuditLogSchema):
    tenant_uid = models.UUIDField(null=True, default=None)
    username = models.CharField(max_length=128)
    url = models.TextField()
    ips = ArrayField(models.GenericIPAddressField(), default=list)
    query_params = models.JSONField(default=dict)
    payload = models.JSONField(default=dict)
    ok = models.BooleanField(default=True)
    error = models.JSONField(default=dict)
    result = models.JSONField(default=dict)
    response_size = models.PositiveIntegerField(default=0)
    type = models.PositiveSmallIntegerField(choices=SECURITY_LOG_TYPE_CHOICE)
    duration = models.PositiveIntegerField(default=0)
    note = models.TextField(default="")

    def __str__(self) -> str:
        return self.target

    class Meta:
        db_table = "audit_logs"
        ordering = ["-id"]
