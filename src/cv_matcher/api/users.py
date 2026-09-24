from typing import Annotated

from fastapi import APIRouter, Depends

from cv_matcher.api.deps import get_current_user
from cv_matcher.models.user import User
from cv_matcher.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user
