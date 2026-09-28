from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=6, max_length=128)
    phone: str = Field(default="", max_length=30)


class ForgotPasswordRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class ResetPasswordRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    reset_token: str = Field(min_length=20, max_length=128)
    new_password: str = Field(min_length=6, max_length=128)