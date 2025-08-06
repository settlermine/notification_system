import psycopg
from structlog import get_logger
from config import settings

logger = get_logger(__name__)


def init_db():
    logger.info("Initializing database...")
    with psycopg.Connection.connect(settings.POSTGRES_CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"""CREATE TABLE users (
                        id SERIAL PRIMARY KEY,
                        email VARCHAR(255) UNIQUE,
                        telegram_id BIGINT UNIQUE,
                        phone_number VARCHAR(20) UNIQUE

                        CONSTRAINT email_check CHECK (email ~* '{settings.EMAIL_REGEX}'),
        
                        CONSTRAINT phone_number_check CHECK (phone_number ~* '{settings.PHONE_NUMBER_REGEX}')
                    );"""
                )
            except Exception as e:
                logger.error("Error initializing tables", error=str(e))
            else:
                logger.info("Database initialized succesfully!")


def drop_db():
    logger.warning("Dropping tables...")
    with psycopg.Connection.connect(settings.POSTGRES_CONNECTION_STRING) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("DROP TABLE users;")
            except Exception as e:
                logger.error("Error dropping tables", error=str(e))
            else:
                logger.info("Tables dropped succesfully!")
