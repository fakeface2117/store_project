import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger

from api.metadata.tags_metadata import tags_metadata
from src.api.v1.users.routers_users import users_router
from src.api.v1.users.login_handler import login_router
from src.core.config import Settings
from src.db import pg_session

app = FastAPI(
    docs_url='/api/store/openapi',
    openapi_url='/api/store/openapi.json'
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="STORE api",
        version="1.0.0",
        description="Store project",
        routes=app.routes,
        tags=tags_metadata
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.on_event('startup')
async def startup():
    pg_engine = create_async_engine(
        url=Settings().CONNECTION_STRING,
        future=True,
        echo=False
    )
    logger.info("Success create sqlalchemy engine.")

    pg_session.SessionLocal = sessionmaker(
        bind=pg_engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False
    )


@app.on_event('shutdown')
async def shutdown():
    pass


app.include_router(users_router, prefix='/api/store/v1/users')
app.include_router(login_router, prefix='/api/store/v1/login')

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8081,
        reload=True
    )
