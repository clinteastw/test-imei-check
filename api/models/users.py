import datetime

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database import Base


class APIUser(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "api_users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    registered_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    
    email: Mapped[str] = mapped_column(
            String(length=320), unique=True, index=True, nullable=False
        )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
