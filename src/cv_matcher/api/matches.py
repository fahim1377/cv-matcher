import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cv_matcher.api.deps import DbSession, get_current_user
from cv_matcher.models.cv import CV
from cv_matcher.models.job import Job
from cv_matcher.models.user import User
from cv_matcher.schemas.match import MatchResult, SkillGapResult
from cv_matcher.services.skills import extract_skills

router = APIRouter(prefix="/matches", tags=["matches"])


async def _get_owned_cv_and_job(
    db: AsyncSession, current_user: User, cv_id: uuid.UUID, job_id: uuid.UUID
) -> tuple[CV, Job]:
    cv = await db.get(CV, cv_id)
    if cv is None or cv.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV not found")

    job = await db.get(Job, job_id)
    if job is None or job.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    return cv, job


@router.get("/{cv_id}/{job_id}", response_model=MatchResult)
async def get_match(
    cv_id: uuid.UUID,
    job_id: uuid.UUID,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> MatchResult:
    cv, job = await _get_owned_cv_and_job(db, current_user, cv_id, job_id)

    distance = await db.scalar(
        select(CV.embedding.cosine_distance(job.embedding)).where(CV.id == cv_id)
    )
    assert distance is not None

    return MatchResult(cv_id=cv_id, job_id=job_id, score=1 - distance)


@router.get("/{cv_id}/{job_id}/skills", response_model=SkillGapResult)
async def get_skill_gap(
    cv_id: uuid.UUID,
    job_id: uuid.UUID,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> SkillGapResult:
    cv, job = await _get_owned_cv_and_job(db, current_user, cv_id, job_id)

    missing_skills = extract_skills(job.raw_text) - extract_skills(cv.raw_text)

    return SkillGapResult(cv_id=cv_id, job_id=job_id, missing_skills=sorted(missing_skills))
