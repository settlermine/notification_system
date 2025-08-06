from senders.base import BaseSender
from structlog import get_logger
from models import User
from senders.exceptions import CannotSendNotificationError
from twilio.rest import Client
from config import settings


logger = get_logger(__name__)


class SmsSender(BaseSender):
    async def send_notification(user: User, content: str) -> None:
        logger.info("Sending notification to user via sms")

        if user.phone_number is None:
            raise CannotSendNotificationError("Parameter phone_number of User is empty")

        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                to=user.phone_number,
                from_=settings.TWILIO_PHONE_NUMBER,
                body=content,
            )
        except Exception as e:
            raise CannotSendNotificationError(
                f"Error sending message via sms: {str(e)}"
            ) from e
