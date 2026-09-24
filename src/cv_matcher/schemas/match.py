import uuid

from pydantic import BaseModel


class MatchResult(BaseModel):
    cv_id: uuid.UUID
    job_id: uuid.UUID
    score: float
