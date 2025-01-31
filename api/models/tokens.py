import uuid

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, async_session_maker


class APIToken(Base):
    __tablename__ = "api_tokens"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)
    api_user_id: Mapped[int] = mapped_column(ForeignKey("api_users.id"))
        
    @classmethod
    async def get_or_create_token(cls, user_id: int) -> str:
        async with async_session_maker() as session:
            query = await session.execute(select(cls).where(cls.api_user_id == user_id))
            existing_token = query.scalar_one_or_none()
            if existing_token:
                return existing_token.token
            
            new_token = str(uuid.uuid4())
            api_token = cls(token=new_token, api_user_id=user_id)
            session.add(api_token)
            await session.commit()
            return new_token
        
    @classmethod
    async def get_by_token_value(cls, token_value: str) -> "APIToken":
        async with async_session_maker() as session:
            query = (select(APIToken).where(APIToken.token == token_value))
            result = await session.execute(query)
            token = result.scalar_one_or_none()
            return token
        
    @classmethod
    async def add_admin_token(cls, token: str) -> str:
        async with async_session_maker() as session:
            token_exists = cls.get_by_token_value(token)
            if not token_exists:
                admin_token = cls(token=token, api_user_id=2)
                session.add(admin_token)
                await session.commit()