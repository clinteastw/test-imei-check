from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, async_session_maker


class TgUser(Base):
    __tablename__ = "tg_users"
    
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    
    @classmethod
    async def check_user_in_whitelist(cls, tg_id: int) -> bool:
        async with async_session_maker() as session:
            query = await session.execute(
                select(cls).where(cls.tg_id == tg_id)
            )
            user = query.scalar_one_or_none()
    
            return user is not None
       
    @classmethod
    async def get_user_from_whitelist(cls, tg_id: int) -> "TgUser":
        async with async_session_maker() as session:
            query = await session.execute(
                select(cls).where(cls.tg_id == tg_id)
            )
            tg_user = query.scalar_one_or_none()
            return tg_user
        
    @classmethod
    async def add_user_to_whitelist(cls, tg_id: int) -> "TgUser":
        async with async_session_maker() as session:
            new_user = cls(tg_id=tg_id)
            session.add(new_user)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_user

    @classmethod
    async def add_users_to_whitelist(cls, users: tuple[int]) -> "TgUser":
        async with async_session_maker() as session:
            for user_tg_id in users:
                if not await cls.get_user_from_whitelist(user_tg_id):
                    new_user = cls(tg_id=user_tg_id)
                    session.add(new_user)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
