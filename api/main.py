import uvicorn
import asyncio
from fastapi import FastAPI

from api.auth.auth import auth_backend, fastapi_users
from api.auth.schemas import UserCreate, UserRead

from .router import api_router

app = FastAPI()

app.include_router(api_router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

async def start_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(start_fastapi())