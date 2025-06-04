from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Security
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware    # ← ВАЖНО!
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.db import get_async_session
from app.schemas import UserCreate, UserOut
from app.models import User


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # или ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Security(oauth2_scheme), db: AsyncSession = Depends(get_async_session)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
    try:
        payload = jwt.decode(token, "SUPER_SECRET_KEY_CHANGE_ME", algorithms=["HS256"])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    q = await db.execute(select(User).filter_by(email=email))
    user = q.scalars().first()
    if user is None:
        raise credentials_exception
    return user.email

@app.post("/register", response_model=UserOut)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_async_session)):
    existing = await db.execute(select(User).filter_by(email=user.email))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = User(
        email=user.email,
        hashed_password=user.password,  # Подключи реальное хэширование!
        created_at=datetime.utcnow(),
        subscription_status="free",
        subscription_expiry=None
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_session)):
    q = await db.execute(select(User).filter_by(email=form_data.username))
    user = q.scalars().first()
    if not user or user.hashed_password != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token_data = {
        "sub": user.email,
    }
    access_token = jwt.encode(token_data, "SUPER_SECRET_KEY_CHANGE_ME", algorithm="HS256")
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/subscription/status")
async def subscription_status(
    db: AsyncSession = Depends(get_async_session),
    user_email: str = Depends(get_current_user)
):
    q = await db.execute(select(User).filter_by(email=user_email))
    user = q.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Автоматически переводим в expired, если подписка истекла
    if user.subscription_status == "premium" and user.subscription_expiry:
        if user.subscription_expiry < datetime.utcnow():
            user.subscription_status = "expired"
            await db.commit()
    return {
        "subscription_status": user.subscription_status,
        "subscription_expiry": (
            user.subscription_expiry.isoformat() if user.subscription_expiry else None
        )
    }

@app.post("/api/solve/text")
async def solve_text_endpoint(
    payload: dict,
    db: AsyncSession = Depends(get_async_session),
    user_email: str = Depends(get_current_user),
):
    q = await db.execute(select(User).filter_by(email=user_email))
    user = q.scalars().first()
    if user.subscription_status != "premium":
        # Логика лимита для free/expired (можно pass для MVP)
        pass
    return {"answer": "Пример ответа"}

@app.post("/api/solve/image")
async def solve_image(
    task: str = "",
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
    user_email: str = Depends(get_current_user)
):
    return {
        "answer": f"Файл {file.filename} успешно принят для задачи: {task}"
    }

@app.post("/subscription/activate_premium")
async def activate_premium(
    db: AsyncSession = Depends(get_async_session),
    user_email: str = Depends(get_current_user)
):
    q = await db.execute(select(User).filter_by(email=user_email))
    user = q.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.subscription_status = "premium"
    user.subscription_expiry = datetime.utcnow() + timedelta(days=31)
    await db.commit()
    return {"status": "ok", "message": "Premium activated"}
