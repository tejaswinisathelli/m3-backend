from enum import Enum
from pydantic import BaseModel


class UserRole(str, Enum):
    ADMIN = "Admin"
    INSPECTOR = "Inspector"
    VIEWER = "Viewer"


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    message: str
    username: str
    role: UserRole | None = None
    authenticated: bool
    access_token: str | None = None