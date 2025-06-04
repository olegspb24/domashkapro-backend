from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# --- путь к файлу базы <project_root>/db.sqlite -----------------
DB_PATH = Path(__file__).resolve().parent.parent / "db.sqlite"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH.as_posix()}"

# --- Base для моделей ------------------------------------------
class Base(DeclarativeBase):
    pass

# --- Engine и Factory session ----------------------------------
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # можно True, чтобы видеть SQL в консоли
    future=True,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

from sqlalchemy.ext.asyncio import AsyncSession

async def get_async_session() -> AsyncSession:
    """
    FastAPI-зависимость для получения асинхронной сессии.
    """
    async with AsyncSessionLocal() as session:
        yield session
