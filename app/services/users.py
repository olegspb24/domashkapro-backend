# app/services/users.py
from typing import Optional
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.models import User

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)


def verify_password(raw: str, hashed: str) -> bool:
    return pwd_ctx.verify(raw, hashed)


# ---------- CRUD ------------

async def get_user_by_email(
    session: AsyncSession,
    email: str,
) -> Optional[User]:
    result = await session.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    email: str,
    password: str,
) -> User:
    hashed = hash_password(password)
    stmt = insert(User).values(email=email, hashed_password=hashed)
    await session.execute(stmt)
    await session.commit()
    # Вернём объект для использования в коде
    return User(id=None, email=email, hashed_password=hashed)  # id появится после refresh
