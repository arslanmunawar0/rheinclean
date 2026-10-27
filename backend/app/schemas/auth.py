from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=200)

    def normalized_email(self) -> str:
        return str(self.email).strip().lower()


class SessionState(BaseModel):
    authenticated: bool
    csrf_token: str
