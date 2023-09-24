from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.api.v1.users.resp_models import Token
from src.services.auth_users import AuthUser, get_auth_users_service
from src.security.tokens import UserTokens
from src.core.config import Settings

login_router = APIRouter()
login_tags: str = 'login'


@login_router.post(
    path='/token',
    tags=[login_tags],
    responses={
        200: {
            "description": "OK",
        },
        404: {
            "description": "Not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Not found"}
                }
            },
        },
    }
)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthUser = Depends(get_auth_users_service)
):
    user = await auth_service.authenticate_user(user_email=form_data.username, user_password=form_data.password)
    if type(user) == HTTPException:
        raise HTTPException(
            status_code=user.status_code,
            detail=user.detail
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect user name or password.'
        )
    access_token_expires = timedelta(minutes=Settings().ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: str = UserTokens.create_access_token(
        data={"sub": user.user_email, "user_id": str(user.user_id)},
        expires_delta=access_token_expires
    )
    return Token(
        access_token=access_token,
        token_type="bearer"
    )
