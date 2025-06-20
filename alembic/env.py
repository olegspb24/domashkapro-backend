import asyncio
from logging.config import fileConfig
from pathlib import Path
from sqlalchemy import create_engine, pool
from alembic import context

# --- добавляем импорт моделей ---
from app.models import Base  # Base = declarative_base()

# -------------------------------------------------------------------
# Читаем alembic.ini
# -------------------------------------------------------------------
config = context.config
fileConfig(config.config_file_name)

# -------------------------------------------------------------------
# 1) Берём URL из alembic.ini, но убираем "+aiosqlite"
# 2) Регистрируем metadata
# -------------------------------------------------------------------
raw_url: str = config.get_main_option("sqlalchemy.url")
sync_url = raw_url.replace("+aiosqlite", "")  # ➜ 'sqlite:///./db.sqlite'
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """offline mode: генерируем SQL, не коннектясь к БД"""
    context.configure(
        url=sync_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """online mode: подключаемся синхронным движком"""
    connectable = create_engine(
        sync_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
