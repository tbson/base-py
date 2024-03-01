import abc
from typing import Optional

from type.general import Condition
from type.result import Result
from type.schema import OtpSchema, TrustedTargetSchema

ExtraData = Optional[dict[str, str]]


class Verify(abc.ABC):
    @abc.abstractmethod
    def get_otp(self, condition: Condition) -> Result[OtpSchema]:
        pass

    @abc.abstractmethod
    def create_otp(
        self,
        target: str,
        type: int,
        ips: list[str],
        extra_data: Optional[dict[str, str]] = None,
    ) -> Result[OtpSchema]:
        pass

    @abc.abstractmethod
    def verify_otp(
        self, verify_id: str, verify_code: str, for_checking: bool = False
    ) -> Result[OtpSchema]:
        pass

    @abc.abstractmethod
    def is_trusted_target(self, target: str) -> bool:
        pass

    @abc.abstractmethod
    def get_otp_email_input(self, otp: OtpSchema) -> tuple[str, str, str]:
        pass

    @abc.abstractmethod
    def set_trusted_target(self, target: str) -> Result[TrustedTargetSchema]:
        pass
