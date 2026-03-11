from pydantic import BaseModel


class SignUpRequest(BaseModel):
    email: str
    username: str
    password: str


class SignInRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
