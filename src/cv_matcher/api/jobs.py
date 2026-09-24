import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select

from cv_matcher.api.deps import DbSession, get_current_user
from cv_matcher.models.job import Job
from cv_matcher.models.user import User
from cv_matcher.schemas.job import JobCreate, JobRead
from cv_matcher.services.embeddings import embed_text

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_in: JobCreate,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> Job:
    embedding = await asyncio.to_thread(embed_text, job_in.raw_text)
    job = Job(
        owner_id=current_user.id,
        title=job_in.title,
        raw_text=job_in.raw_text,
        embedding=embedding,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


@router.get("", response_model=list[JobRead])
async def list_my_jobs(
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[Job]:
    result = await db.execute(select(Job).where(Job.owner_id == current_user.id))
    return list(result.scalars().all())
