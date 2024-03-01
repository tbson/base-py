from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from interface.email import Email
from type.email import EmailBody, EmailSubject, EmailTo
from type.result import Result
from util.async_util import async_task
from util.error_util import ErrorUtil


class EmailService(Email):
    def send_email(
        self, subject: EmailSubject, body: EmailBody, to: EmailTo
    ) -> Result[str]:
        try:
            if settings.EMAIL_ENABLE is not True or settings.TESTING:
                return ("email not send", True)
            if not isinstance(to, list):
                to = [str(to)]
            email = EmailMultiAlternatives(
                subject, body, settings.DEFAULT_FROM_EMAIL, to
            )
            email.content_subtype = "html"
            email.attach_alternative(body, "text/html")

            result = str(email.send())
            return (result, True)
        except Exception as e:  # skipcq: Sending email can be failed
            # print(ErrorUtil.return_exception(e))
            return ErrorUtil.format(e), False

    @async_task
    def send_email_async(
        self, subject: EmailSubject, body: EmailBody, to: EmailTo
    ) -> None:
        self.send_email(subject, body, to)
