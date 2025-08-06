from models import User


class BaseSender:
    async def send_notification(user: User, content: str) -> None:
        raise NotImplementedError
