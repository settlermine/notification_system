from .base import BaseSender
from .email import EmailSender
from .sms import SmsSender
from .telegram import TelegramSender
from .exceptions import SenderDoesNotExistError

from config.settings import TELEGRAM, EMAIL, SMS



def get_notification_sender(destination: str) -> BaseSender:
    if destination == EMAIL:
        return EmailSender
    if destination == TELEGRAM:
        return TelegramSender
    if destination == SMS:
        return SmsSender

    raise SenderDoesNotExistError(f"Cannot find sender for destination {destination}")
