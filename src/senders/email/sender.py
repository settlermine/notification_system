from senders.base import BaseSender
from senders.exceptions import CannotSendNotificationError
from structlog import get_logger
from models import User
from aiosmtplib import SMTP
from email.mime.text import MIMEText
from config import settings

logger = get_logger(__name__)


class EmailSender(BaseSender):
    async def send_notification(user: User, content: str) -> None:
        logger.info("Sending notification to user via email")
        if user.email is None:
            raise CannotSendNotificationError("Parameter email of User is empty")

        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = settings.EMAIL_SUBJECT
        msg["From"] = settings.SMTP_LOGIN
        msg["To"] = user.email

        try:
            smtp = SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT)
            await smtp.connect()
            await smtp.login(settings.SMTP_LOGIN, settings.SMTP_PASSWORD)
            await smtp.send_message(msg)
            await smtp.quit()
        except Exception as e:
            raise CannotSendNotificationError(
                f"Error sending message via email: {str(e)}"
            ) from e
