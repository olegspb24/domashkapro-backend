# app/core/auth.py
import os, time
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_async_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User

# Секрет для подписи токена
JWT_SECRET = os.getenv("JWT_SECRET", "SUPER_SECRET_KEY_CHANGE_ME")
ALGO = "HS256"
EXPIRE_SECONDS = 60 * 60 * 24  # 24h

# Простое хранилище пользователей в БД

# Генерация токена

def create_access_token(email: str) -> str:
    payload = {"sub": email, "exp": int(time.time()) + EXPIRE_SECONDS}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGO)

# Верификация токена

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGO])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# FastAPI dependency
bearer_scheme = HTTPBearer()

async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_async_session),
) -> User:
    email = verify_token(creds.credentials)
    # Проверяем, что пользователь есть в БД
    q = await db.execute(select(User).filter_by(email=email))
    user = q.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
