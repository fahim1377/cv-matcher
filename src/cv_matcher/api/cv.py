import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import select

from cv_matcher.api.deps import DbSession, get_current_user
from cv_matcher.models.cv import CV
from cv_matcher.models.user import User
from cv_matcher.schemas.cv import CVCreate, CVRead
from cv_matcher.services.embeddings import embed_text

router = APIRouter(prefix="/cv", tags=["cv"])


@router.post("", response_model=CVRead, status_code=status.HTTP_201_CREATED)
async def create_cv(
    cv_in: CVCreate,
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> CV:
    embedding = await asyncio.to_thread(embed_text, cv_in.raw_text)
    cv = CV(owner_id=current_user.id, raw_text=cv_in.raw_text, embedding=embedding)
    db.add(cv)
    await db.commit()
    await db.refresh(cv)
    return cv


@router.get("", response_model=list[CVRead])
async def list_my_cvs(
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[CV]:
    result = await db.execute(select(CV).where(CV.owner_id == current_user.id))
    return list(result.scalars().all())
