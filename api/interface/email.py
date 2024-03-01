import abc

from type.email import EmailBody, EmailSubject, EmailTo


class Email(abc.ABC):
    @abc.abstractmethod
    def send_email_async(
        self, subject: EmailSubject, body: EmailBody, to: EmailTo
    ) -> None:
        pass
