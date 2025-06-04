from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    # Новые поля для подписки
    subscription_status = Column(String, default="free", nullable=False)  # free/premium/expired
    subscription_expiry = Column(DateTime, nullable=True)

    # Оставь все связи и логику ниже, если были
    # Например, если есть задачи или items:
    # items = relationship("Item", back_populates="owner")

# Остальные модели, если есть, оставляй без изменений
