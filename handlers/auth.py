from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_auth_service, get_user_service
from exception import UserNotCorrectPasswordException, UserNotFoundException
from schema import UserCreateSchema, UserLoginSchema
from service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserLoginSchema)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        return auth_service.login(body.username, body.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.detail)
