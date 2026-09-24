import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CVCreate(BaseModel):
    raw_text: str = Field(min_length=1)


class CVRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    raw_text: str
    created_at: datetime
