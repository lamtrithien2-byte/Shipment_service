from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from sqlalchemy.orm import Session

from app.db.db_database import get_db
from app.services import service_auth

router = APIRouter(prefix="/api/v1/customers", tags=["auth"])


class LoginType(str, Enum):
    CUSTOMER_PASSWORD = "CUSTOMER_PASSWORD"


class LoginRequest(BaseModel):
    login_type: LoginType
    customer_email: str | None = None
    customer_mobile: str | None = None
    customer_password: str = Field(min_length=1)

    @model_validator(mode="after")
    def check_email_or_mobile(self):
        has_email = bool(self.customer_email)
        has_mobile = bool(self.customer_mobile)

        if has_email == has_mobile:
            raise ValueError("Chi su dung 1 trong 2: customer_email hoac customer_mobile")

        return self


@router.post("/login")
def login(
    body: LoginRequest,
    app_code: str = Header(alias="APP-CODE"),
    login_type: LoginType = Header(alias="LOGIN-TYPE"),
    accept: str = Header(default="application/json", alias="Accept"),
    db: Session = Depends(get_db),
):
    return service_auth.login(db, body, app_code, login_type, accept)
