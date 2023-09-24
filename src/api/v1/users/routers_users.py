import uuid
from typing import Union

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.users.resp_models import (CreateUserRequest,
                                          SelectUserResponse,
                                          UpdateUserRequest, UserIdResponse)
from src.services.users import UsersService, get_users_service

users_router = APIRouter()
users_tags: str = 'users'


@users_router.post(
    path='/create',
    tags=[users_tags],
    responses={
        200: {
            "description": "User created.",
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
async def create_user(
        input_user_data: CreateUserRequest,
        users_service: UsersService = Depends(get_users_service)
) -> UserIdResponse:
    """Create new user"""
    result: Union[UserIdResponse, HTTPException] = await users_service.create_user(
        name=input_user_data.name,
        lastname=input_user_data.lastname,
        surname=input_user_data.surname,
        country=input_user_data.country,
        user_email=input_user_data.user_email,
        user_password=input_user_data.user_pass,
        consent_to_mailing=input_user_data.consent_to_mailing
    )
    if type(result) == HTTPException:
        raise HTTPException(status_code=result.status_code, detail=result.detail)
    return result


@users_router.get(
    path='/read',
    tags=[users_tags],
    responses={
        200: {
            "description": "User selected.",
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
async def get_user(
        user_uuid: uuid.UUID,
        users_service: UsersService = Depends(get_users_service)
) -> SelectUserResponse:
    result: Union[SelectUserResponse, HTTPException] = await users_service.get_user_by_id(
        user_id=user_uuid
    )
    if type(result) == HTTPException:
        raise HTTPException(status_code=result.status_code, detail=result.detail)
    return result


@users_router.patch(
    path='/update',
    tags=[users_tags],
    responses={
        200: {
            "description": "User was updated.",
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
async def update_user(
        user_uuid: uuid.UUID,
        updated_params: UpdateUserRequest,
        users_service: UsersService = Depends(get_users_service)
) -> UserIdResponse:
    updated_user_params = updated_params.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(status_code=422, detail="Mast be least one parameter for user update.")
    user: Union[SelectUserResponse, HTTPException] = await users_service.get_user_by_id(user_id=user_uuid)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_uuid} not found.")
    result: Union[UserIdResponse, HTTPException] = await users_service.update_user_by_id(
        user_id=user_uuid,
        **updated_user_params
    )
    if type(result) == HTTPException:
        raise HTTPException(status_code=result.status_code, detail=result.detail)
    return result


@users_router.delete(
    path='/delete',
    tags=[users_tags],
    responses={
        200: {
            "description": "User was deleted.",
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
async def delete_user(
        user_uuid: uuid.UUID,
        users_service: UsersService = Depends(get_users_service)
) -> UserIdResponse:
    result: Union[UserIdResponse, HTTPException] = await users_service.delete_user_by_id(user_id=user_uuid)
    if type(result) == HTTPException:
        raise HTTPException(status_code=result.status_code, detail=result.detail)
    return result
