from db.users import get_user_by_id
from senders import (
    get_notification_sender,
    CannotSendNotificationError,
    SenderDoesNotExistError,
)
from typing import Optional
from models import User
from config.settings import DESTINATIONS
from structlog import get_logger


logger = get_logger(__name__)


async def send_notification(
    user_id: int, destination: Optional[str], content: str
) -> bool:
    if user_id is None:
        logger.error('Cannot send notification: user_id was not provided')
        return False

    if content is None:
        logger.error('Cannot send notification: content was not provided')
        return False
    
    try:
        user = await get_user_by_id(user_id=user_id)
    except Exception as e:
        logger.error('Error while getting user from db', error=str(e))
        return False
    
    if user is None:
        logger.error('Cannot send notification: User does not exist', user_id=user_id)
        return False

    if destination is not None:
        channels = [destination] + [d for d in DESTINATIONS if d != destination]
    else:
        logger.info(
            'Destination was not provided. Using default',
            default_destination=DESTINATIONS[0],
        )
        channels = DESTINATIONS

    for channel in channels:
        try:
            await _send_notification(user, channel, content)
        except CannotSendNotificationError as e:
            logger.error(
                'Failed to send notification', destination=channel, error=str(e)
            )
            continue
        except SenderDoesNotExistError as e:
            logger.error(
                'Destination is not supported', destination=channel, error=str(e)
            )
            continue
        else:
            logger.info('Notification sent successfully', destination=channel)
            return True

    logger.info('Failed to send notification via any channel')
    return False


async def _send_notification(user: User, destination: str, content: str):
    notification_sender = get_notification_sender(destination=destination)
    await notification_sender.send_notification(user, content)
