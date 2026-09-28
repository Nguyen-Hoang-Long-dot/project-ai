from datetime import datetime, timedelta, UTC
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.core.config import settings
from app.core.security import verify_password, create_access_token, get_current_user_payload, get_password_hash
from app.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest, UserRegister
from app.schemas.user import UserLogin, Token, UserResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])
reset_tokens: dict[str, tuple[str, datetime]] = {}


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại.")

    user = User(
        username=payload.username,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    response = {"message": "Nếu tài khoản tồn tại, hướng dẫn đặt lại mật khẩu đã được tạo."}
    if not user:
        return response

    reset_token = secrets.token_urlsafe(32)
    reset_tokens[payload.username] = (reset_token, datetime.now(UTC) + timedelta(minutes=15))
    if settings.ENV == "development":
        response["reset_token"] = reset_token
    return response


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    stored = reset_tokens.get(payload.username)
    if not stored or stored[0] != payload.reset_token or stored[1] < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="Mã đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.")

    user = db.query(User).filter(User.username == payload.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Không thể đặt lại mật khẩu cho tài khoản này.")
    user.hashed_password = get_password_hash(payload.new_password)
    db.commit()
    reset_tokens.pop(payload.username, None)
    return {"message": "Đặt lại mật khẩu thành công. Bạn có thể đăng nhập ngay bây giờ."}

@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tài khoản hoặc mật khẩu không chính xác.")
    
    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role.value,
        "username": user.username
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user_payload), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_user["sub"]).first()
    return user