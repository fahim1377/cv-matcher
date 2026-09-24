import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from cv_matcher.api.deps import DbSession, get_current_user
from cv_matcher.models.cv import CV
from cv_matcher.models.job import Job
from cv_matcher.models.user import User
from cv_matcher.schemas.match import MatchResult

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/{cv_id}/{job_id}", response_model=MatchResult)
async def get_match(
    cv_id: uuid.UUID,
    job_id: uuid.UUID,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> MatchResult:
    cv = await db.get(CV, cv_id)
    if cv is None or cv.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV not found")

    job = await db.get(Job, job_id)
    if job is None or job.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    distance = await db.scalar(
        select(CV.embedding.cosine_distance(job.embedding)).where(CV.id == cv_id)
    )
    assert distance is not None

    return MatchResult(cv_id=cv_id, job_id=job_id, score=1 - distance)
