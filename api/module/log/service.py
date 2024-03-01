import sys
from datetime import timedelta
from typing import Optional, Union, cast

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from interface.log import Log
from module.account.service import AccountService
from module.log.const import AuditLogType
from module.log.models import AuditLog, EmailLog
from pydantic import BaseModel
from type.general import Condition, QuerySet
from type.result import ErrorValue, Result
from type.schema import AuditLogSchema, EmailLogSchema, UserSchema
from util.date_util import DateUtil
from util.error_util import ErrorUtil
from util.framework.schema_util import SchemaUtil
from util.map_util import MapUtil
from util.pwd_util import PwdUtil
from util.request_util import RequestUtil


class LogService(Log):
    def get_list_email_log(
        self, condition: Condition, limit: Optional[int] = None, order_by: str = "-id"
    ) -> Result[QuerySet[EmailLogSchema]]:
        try:
            query = EmailLog.objects.filter(**condition).order_by(order_by)
            if limit is not None:
                query = query[:limit]
            return query, True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_email_log(self, condition: Condition) -> Result[EmailLogSchema]:
        try:
            return EmailLog.objects.get(**condition), True
        except EmailLog.DoesNotExist:
            err_msg = _("email log does not exist")
            return ErrorUtil.format(err_msg), False

    def create_email_log(self, condition: Condition) -> Result[EmailLogSchema]:
        try:
            return EmailLog.objects.create(**condition), True
        except Exception as e:
            return ErrorUtil.format(e), False

    def update_email_log(
        self, condition: Condition, data: dict
    ) -> Result[EmailLogSchema]:
        result, ok = self.get_email_log(condition)
        if not ok:
            return result, False
        email_log = result
        return SchemaUtil.update(email_log, data)

    def delete_email_log(self, condition: Condition) -> Result[list[int]]:
        try:
            email_logs = EmailLog.objects.filter(**condition)
            email_logs.delete()
            return list(email_logs.values_list("id", flat=True)), True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_list_security_log(
        self, condition: Condition, limit: Optional[int] = None, order_by: str = "-id"
    ) -> Result[QuerySet[AuditLogSchema]]:
        try:
            query = AuditLog.objects.filter(**condition).order_by(order_by)
            if limit is not None:
                query = query[:limit]
            return query, True
        except Exception as e:
            return ErrorUtil.format(e), False

    def get_security_log(self, condition: Condition) -> Result[AuditLogSchema]:
        try:
            return AuditLog.objects.get(**condition), True
        except AuditLog.DoesNotExist:
            err_msg = _("audit log does not exist")
            return ErrorUtil.format(err_msg), False

    def create_audit_log(self, condition: Condition) -> Result[AuditLogSchema]:
        try:
            return AuditLog.objects.create(**condition), True
        except Exception as e:
            print(e)
            return ErrorUtil.format(e), False

    def update_security_log(
        self, condition: Condition, data: dict
    ) -> Result[AuditLogSchema]:
        result, ok = self.get_security_log(condition)
        if not ok:
            return result, False
        security_log = result
        return SchemaUtil.update(security_log, data)

    def delete_security_log(self, condition: Condition) -> Result[list[int]]:
        try:
            security_logs = AuditLog.objects.filter(**condition)
            security_logs.delete()
            return list(security_logs.values_list("id", flat=True)), True
        except Exception as e:
            return ErrorUtil.format(e), False

    def reached_login_fail_limit(self, username: str) -> Result[None]:
        err_msg = _("user reached daily login fail limit")
        result, ok = self.get_list_security_log(
            dict(
                type=AuditLogType.LOGIN,
                username=username,
                ok=False,
                created_at__date=DateUtil.today(),
            )
        )
        if ok and len(result) >= settings.MAX_DAILY_LOGIN_FAIL:
            return ErrorUtil.format(err_msg), False
        return (None, True) if ok else (ErrorUtil.format(err_msg), False)

    def is_use_old_password(self, username: str, password: str) -> Result[None]:
        err_msg = _("user use old password")
        result, ok = self.get_list_security_log(
            dict(
                type__in=[AuditLogType.CHANGE_PWD, AuditLogType.RESET_PWD],
                username=username,
                ok=True,
            ),
            limit=settings.MIN_REUSE_PWD,
        )
        if not ok:
            return result, False
        result = cast(QuerySet[AuditLogSchema], result)
        return next(
            (
                (ErrorUtil.format(err_msg), False)
                for log in result
                if PwdUtil.check_password(password, log.note)
            ),
            (None, True),
        )


class AuditLogService:
    def __init__(self, request: HttpRequest, payload: Optional[dict] = None) -> None:
        self.request = request
        if payload is None:
            payload = {}
        self.start_time = DateUtil.now()
        self.url = request.path
        self.ips = RequestUtil.get_ips(request.headers)
        self.query_params = RequestUtil.get_query_params(request.get_full_path())
        self.payload = MapUtil.mask_password_related(payload)

    def __write_log(
        self,
        log_type: int,
        username: str,
        logic_result: Union[BaseModel, ErrorValue],
        ok: bool,
        note: str,
    ) -> Result[AuditLogSchema]:
        log_service = LogService()
        tenant_uid = None
        user_result, user_ok = AccountService().get_user(dict(username=username))
        if not user_ok:
            return user_result, False
        user = cast(UserSchema, user_result)
        tenant_uid = user.tenant.uid if user.tenant else None

        duration_delta: timedelta = DateUtil.now() - self.start_time
        duration = int(duration_delta.total_seconds() * 1000)

        result = {}
        error: ErrorValue = {}
        response_size = sys.getsizeof(str(logic_result))
        if ok:
            result = (
                logic_result.dict() if hasattr(logic_result, "dict") else logic_result
            )
            error = {}
        else:
            result = {}
            error = logic_result

        condition: Condition = dict(
            tenant_uid=tenant_uid,
            username=username,
            url=self.url,
            ips=self.ips,
            query_params=self.query_params,
            payload=self.payload,
            ok=ok,
            error=error,
            result=result,
            response_size=response_size,
            type=log_type,
            duration=duration,
            note=note,
        )
        return log_service.create_audit_log(condition)

    def log_login(
        self,
        logic_result: Union[BaseModel, ErrorValue],
        ok: bool,
        note: str = "",
    ) -> None:
        username = self.payload.get("username", "")

        self.__write_log(
            AuditLogType.LOGIN,
            username,
            logic_result,
            ok,
            note,
        )

    def log_change_pwd(
        self,
        logic_result: Result[BaseModel],
        ok: bool,
        note: str = "",
    ) -> None:
        user = self.request.user
        username = user.username
        password = make_password(note)

        self.__write_log(
            AuditLogType.CHANGE_PWD,
            username,
            logic_result,
            ok,
            password,
        )

    def log_reset_pwd(
        self,
        logic_result: Result[BaseModel],
        ok: bool,
        note: str = "",
    ) -> None:
        username = self.payload.get("username", "")
        password = make_password(note)

        self.__write_log(
            AuditLogType.RESET_PWD,
            username,
            logic_result,
            ok,
            password,
        )
