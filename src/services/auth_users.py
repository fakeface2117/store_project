from functools import lru_cache
from typing import Union

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from src.api.v1.users.resp_models import SelectUserByEmailResponse
from src.db.pg_session import get_db
from src.pkg.storage import models
from src.pkg.hashing.hashing import Hasher


class AuthUser:
    def __init__(self, db: AsyncSession):
        self.db_session = db

    async def __get_user_by_email(
            self,
            user_email: str
    ) -> Union[SelectUserByEmailResponse, None, HTTPException]:
        try:
            query = select(models.Users).where(models.Users.user_email == user_email)
            result = await self.db_session.execute(query)
            selected_user: models.Users = result.scalars().first()
            if not selected_user:
                return None
            return SelectUserByEmailResponse(
                user_id=selected_user.user_id,
                user_email=selected_user.user_email,
                hashed_password=selected_user.hashed_password
            )
        except Exception as ex: # todo разные ошибки
            error_message = f"Error while select user by email = {user_email}: {ex}"
            logger.error(error_message)
            return HTTPException(status_code=402, detail=error_message)
        finally:
            await self.db_session.close()

    async def authenticate_user(
            self,
            user_email: str,
            user_password: str
    ) -> Union[HTTPException, bool, SelectUserByEmailResponse]:
        user = await self.__get_user_by_email(user_email=user_email)
        if not user:
            return False
        if not Hasher.verify_password(plain_password=user_password, hashed_password=user.hashed_password):
            return False
        return user



@lru_cache()
def get_auth_users_service(
        db_session: AsyncSession = Depends(get_db)
) -> AuthUser:
    return AuthUser(db=db_session)
