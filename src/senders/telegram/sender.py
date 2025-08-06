from senders.base import BaseSender
from senders.exceptions import CannotSendNotificationError
from config import settings
from structlog import get_logger
from models import User
import aiohttp

logger = get_logger(__name__)


class TelegramSender(BaseSender):
    async def send_notification(user: User, content: str) -> None:
        logger.info("Sending notification to user via telegram")
        if user.telegram_id is None:
            raise CannotSendNotificationError("Parameter telegram_id of User is empty")

        url = f"https://api.telegram.org/bot{settings.TELEGRAM_API_KEY}/sendMessage"
        data = {"chat_id": user.telegram_id, "text": content}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            raise CannotSendNotificationError(
                f"Error sending message via telegram: {str(e)}"
            ) from e
