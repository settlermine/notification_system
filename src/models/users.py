from pydantic import BaseModel, Field
from typing import Optional
from config.settings import (
    EMAIL_REGEX,
    PHONE_NUMBER_REGEX,
)


class User(BaseModel):
    id: int = Field(gt=0)
    email: Optional[str] = Field(None, pattern=EMAIL_REGEX)
    telegram_id: Optional[int] = Field(None, gt=0)
    phone_number: Optional[str] = Field(None, pattern=PHONE_NUMBER_REGEX)
