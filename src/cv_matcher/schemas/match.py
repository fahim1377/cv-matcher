import uuid

from pydantic import BaseModel


class MatchResult(BaseModel):
    cv_id: uuid.UUID
    job_id: uuid.UUID
    score: float


class SkillGapResult(BaseModel):
    cv_id: uuid.UUID
    job_id: uuid.UUID
    missing_skills: list[str]
