import abc

from type.general import Condition, QuerySet
from type.result import Result
from type.schema import AuditLogSchema, EmailLogSchema


class Log(abc.ABC):
    # @abc.abstractmethod
    # def write_login_log(
    #    self, target: str, error: Optional[ErrorValue], headers: dict
    # ) -> Result[AuditLogSchema]:
    #    pass

    @abc.abstractmethod
    def get_list_email_log(
        self, condition: Condition
    ) -> Result[QuerySet[EmailLogSchema]]:
        pass

    @abc.abstractmethod
    def get_email_log(self, condition: Condition) -> Result[EmailLogSchema]:
        pass

    @abc.abstractmethod
    def create_email_log(self, condition: Condition) -> Result[EmailLogSchema]:
        pass

    @abc.abstractmethod
    def update_email_log(
        self, condition: Condition, data: dict
    ) -> Result[EmailLogSchema]:
        pass

    @abc.abstractmethod
    def delete_email_log(self, condition: Condition) -> Result[list[int]]:
        pass

    # @abc.abstractmethod
    # def delete_pwd_history_log(self, condition: Condition) -> Result[list[int]]:
    #    pass

    @abc.abstractmethod
    def get_list_security_log(
        self, condition: Condition
    ) -> Result[QuerySet[AuditLogSchema]]:
        pass

    @abc.abstractmethod
    def get_security_log(self, condition: Condition) -> Result[AuditLogSchema]:
        pass

    # @abc.abstractmethod
    # def create_security_log(self, condition: Condition) -> Result[AuditLogSchema]:
    #    pass

    @abc.abstractmethod
    def update_security_log(
        self, condition: Condition, data: dict
    ) -> Result[AuditLogSchema]:
        pass

    @abc.abstractmethod
    def delete_security_log(self, condition: Condition) -> Result[list[int]]:
        pass

    @abc.abstractmethod
    def reached_login_fail_limit(self, username: str) -> Result[None]:
        pass

    @abc.abstractmethod
    def is_use_old_password(self, username: str, password: str) -> Result[None]:
        pass
