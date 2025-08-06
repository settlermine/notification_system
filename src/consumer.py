import asyncio
import aio_pika
import aio_pika.abc
import structlog
import uuid
import json

import config.settings as settings
from service import send_notification

logger = structlog.get_logger(__name__)


async def main():
    connection = await aio_pika.connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD,
    )

    async with connection:
        queue_name = "notifications"

        channel: aio_pika.abc.AbstractChannel = await connection.channel()

        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(
            queue_name,
            durable=True,
        )
        logger.info("Service is ready to consume messages")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                message_id = str(uuid.uuid4())
                structlog.contextvars.bind_contextvars(message_id=message_id)

                logger.info("Got new message")
                async with message.process():
                    try:
                        body = json.loads(message.body)
                    except json.decoder.JSONDecodeError as e:
                        logger.error(
                            "Cannot decode message body. Invalid JSON format",
                            error=str(e),
                        )
                        continue

                    user_id = body.get("user_id")
                    destination = body.get("destination")
                    content = body.get("content")

                    await send_notification(user_id, destination, content)


if __name__ == "__main__":
    asyncio.run(main())
