import datetime
import uuid
from functools import lru_cache
from typing import Union

from fastapi import Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from src.api.v1.users.resp_models import UserIdResponse, SelectUserResponse
from src.db.pg_session import get_db
from src.pkg.storage import models
from src.services.abstract.abstract_services import CrudService
from src.pkg.hashing.hashing import Hasher


class UsersService(CrudService):
    """Class that realise CRUD for users table"""

    def __init__(self, db: AsyncSession):
        self.db_session = db

    async def create_user(
            self,
            name: str,
            lastname: Union[str, None],
            surname: str,
            country: str,
            user_email: EmailStr,
            user_password: str,
            consent_to_mailing: bool = False
    ) -> Union[UserIdResponse, HTTPException]:
        """Func for create new user of store."""
        try:
            new_user = models.Users(
                name=name,
                lastname=lastname,
                surname=surname,
                country=country,
                user_email=user_email,
                date_registration=datetime.datetime.now(),
                consent_to_mailing=consent_to_mailing,
                hashed_password=Hasher.get_pass_hash(user_password)
            )
            self.db_session.add(new_user)
            await self.db_session.commit()
            await self.db_session.refresh(new_user)
            logger.info(f"Created new user with id {new_user.user_id}.")
            return UserIdResponse(
                user_id=new_user.user_id
            )

        except Exception as ex:
            error_message = f"Error while create new user: {ex}"
            logger.error(error_message)
            return HTTPException(status_code=402, detail=error_message)

    async def get_user_by_id(
            self,
            user_id: uuid.UUID
    ) -> Union[SelectUserResponse, HTTPException]:
        """Get info about user by id."""
        try:
            query = select(models.Users).where(models.Users.user_id == user_id)
            result = await self.db_session.execute(query)
            selected_user = result.scalars().first()
            if not selected_user:
                return HTTPException(status_code=400, detail="User not found")
            logger.info(f"Success select user with id {selected_user.user_id}")
            return SelectUserResponse(
                user_id=selected_user.user_id,
                name=selected_user.name,
                lastname=selected_user.lastname,
                surname=selected_user.surname,
                country=selected_user.country,
                user_email=selected_user.user_email,
                date_registration=selected_user.date_registration,
                consent_to_mailing=selected_user.consent_to_mailing
            )

        except Exception as ex:
            error_message = f"Error while select user by id = {user_id}: {ex}"
            logger.error(error_message)
            return HTTPException(status_code=402, detail=error_message)
        finally:
            await self.db_session.close()

    async def update_user_by_id(self, user_id, **kwargs) -> Union[UserIdResponse, HTTPException]:
        """Update user info by id."""
        try:
            query = update(models.Users).where(models.Users.user_id == user_id).values(kwargs).returning(
                models.Users.user_id)
            result = await self.db_session.execute(query)
            await self.db_session.commit()
            update_user_id = result.fetchone()
            if update_user_id is not None:
                logger.info(f"Success update user data by id {update_user_id[0]}")
                return UserIdResponse(user_id=update_user_id[0])
            else:
                return HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
        except Exception as ex:
            error_message = f"Error while update user by id = {user_id}: {ex}"
            logger.error(error_message)
            return HTTPException(status_code=402, detail=error_message)
        finally:
            await self.db_session.close()

    async def delete_user_by_id(self, user_id) -> Union[UserIdResponse, HTTPException]:
        """Delete data about user from db by id."""
        try:
            query = select(models.Users).where(models.Users.user_id == user_id)
            try:
                result = await self.db_session.execute(query)
                selected_user = result.scalar_one()
                await self.db_session.delete(selected_user)
                await self.db_session.commit()
                logger.info(f"Success deleted user's info by id {selected_user.user_id}")
                return UserIdResponse(user_id=selected_user.user_id)
            except Exception as ex:
                error_message = f"User not found with id {user_id}: {ex}"
                logger.error(error_message)
                return HTTPException(status_code=404, detail=error_message)
            finally:
                await self.db_session.close()

        except Exception as ex:
            error_message = f"Error while delete user by id = {user_id}: {ex}"
            logger.error(error_message)
            return HTTPException(status_code=402, detail=error_message)


@lru_cache()
def get_users_service(
        db_session: AsyncSession = Depends(get_db)
) -> UsersService:
    return UsersService(db=db_session)
