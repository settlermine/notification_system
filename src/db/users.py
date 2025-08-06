from models import User
from structlog import get_logger
from config import settings
import psycopg


logger = get_logger(__name__)


async def get_user_by_id(user_id: int) -> User | None:
    logger.info("Getting user by id", user_id=user_id)
    async with await psycopg.AsyncConnection.connect(
        settings.POSTGRES_CONNECTION_STRING
    ) as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                "SELECT id, telegram_id, phone_number, email FROM users WHERE id=%s",
                (user_id,),
            )
            result = await cursor.fetchone()

    if not result:
        return

    return User(
        id=result[0],
        telegram_id=result[1],
        phone_number=result[2],
        email=result[3],
    )
