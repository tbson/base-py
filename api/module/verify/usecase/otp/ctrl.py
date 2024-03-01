from typing import cast

from django.http import HttpRequest
from module.account.repo import AccountRepo
from module.verify.const import OtpType
from module.verify.repo import VerifyRepo
from module.verify.usecase.otp.service import OtpService, SendOtpOutput
from module.verify.usecase.otp.validator import (
    ResendOtpInput,
    SendOtpInput,
    VerifyOtpInput,
)
from ninja import Router
from repo.email_repo import EmailRepo
from contract.type.result import ErrorResponse, ErrorValue
from util.request_util import RequestUtil

router = Router()
TAGS = ["verify / OTP"]


@router.post(
    "/send-reset-pwd-otp/",
    tags=TAGS,
    response={200: SendOtpOutput, 400: ErrorValue},
)
def send_reset_pwd_otp(
    request: HttpRequest, data: SendOtpInput
) -> SendOtpOutput | ErrorResponse:
    ips = RequestUtil.get_ips(request.headers)
    otp_type = OtpType.RESET_PWD
    (result, ok) = OtpService.send_otp(AccountRepo(), VerifyRepo(), EmailRepo())(
        data.username, otp_type, ips
    )
    return result if ok else RequestUtil.err(result)


@router.post(
    "/send-signup-otp/",
    tags=TAGS,
    response={200: SendOtpOutput, 400: ErrorValue},
)
def send_signup_otp(
    request: HttpRequest, data: SendOtpInput
) -> SendOtpOutput | ErrorResponse:
    ips = RequestUtil.get_ips(request.headers)
    otp_type = OtpType.SIGNUP
    (result, ok) = OtpService.send_otp(AccountRepo(), VerifyRepo(), EmailRepo())(
        data.username, otp_type, ips
    )
    return result if ok else RequestUtil.err(result)


@router.post(
    "/resend-otp/",
    tags=TAGS,
    response={200: SendOtpOutput, 400: ErrorValue},
)
def resend_otp(
    request: HttpRequest, data: ResendOtpInput
) -> SendOtpOutput | ErrorResponse:
    (result, ok) = OtpService.resend_otp(AccountRepo(), VerifyRepo(), EmailRepo())(
        data.verify_id
    )
    return cast(SendOtpOutput, result) if ok else RequestUtil.err(result)


@router.post(
    "/verify-otp/",
    tags=TAGS,
    response={200: dict, 400: ErrorValue},
)
def verify_otp(request: HttpRequest, data: VerifyOtpInput) -> dict | ErrorResponse:
    (result, ok) = OtpService.verify_otp(VerifyRepo())(data.verify_id, data.verify_code)
    return {} if ok else RequestUtil.err(result)


@router.post(
    "/check-otp/",
    tags=TAGS,
    response={200: dict, 400: ErrorValue},
)
def check_otp(request: HttpRequest, data: VerifyOtpInput) -> dict | ErrorResponse:
    (result, ok) = OtpService.check_otp(VerifyRepo())(data.verify_id, data.verify_code)
    return {} if ok else RequestUtil.err(result)
