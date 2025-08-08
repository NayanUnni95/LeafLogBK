import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings

class MailUtil:
    @staticmethod
    async def email_without_attachment(to_email: str, subject: str, message: str) -> None:
        smtp_server = settings.SMTP_SERVER
        smtp_port = settings.SMTP_PORT
        smtp_username = settings.SMTP_USERNAME
        smtp_password = settings.SMTP_PASSWORD
        from_mail = settings.FROM_MAIL