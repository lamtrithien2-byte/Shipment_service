import base64
import hmac
import json
import os
import time
from hashlib import sha256

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.repositories import repo_customer

APP_CODE = os.getenv("APP_CODE", "TEST-API")
LOGIN_TYPE = "CUSTOMER_PASSWORD"
TOKEN_EXPIRE_SECONDS = 2538000
SECRET_KEY = os.getenv("SECRET_KEY", "shipment-secret-key")


def login(db: Session, data, app_code: str, login_type: str, accept: str):
    if accept != "application/json":
        return error_response(422, "Accept phai la application/json")

    if app_code != APP_CODE:
        return error_response(422, "APP-CODE khong hop le")

    if normalize_login_type(login_type) != LOGIN_TYPE or normalize_login_type(data.login_type) != LOGIN_TYPE:
        return error_response(422, "LOGIN-TYPE khong hop le")

    customer = repo_customer.get_login_customer(db, data.customer_email, data.customer_mobile)
    if customer is None:
        return error_response(-1001, "Khong tim thay tai khoan")

    if data.customer_password != customer.customer_password:
        return error_response(-1002, "Tai khoan hoac mat khau khong dung")

    if not customer.is_active:
        return error_response(-1005, "Tai khoan bi khoa")

    token = create_access_token(customer)
    if not token:
        return error_response(-1010, "Tao token dang nhap khong thanh cong")

    return {
        "success": True,
        "STATUS": "OK",
        "status_code": 200,
        "message": "Dang nhap thanh cong",
        "data": customer_data(customer),
        "access_token": f"Bearer {token}",
        "expire": TOKEN_EXPIRE_SECONDS,
    }


def normalize_login_type(value: str) -> str:
    if hasattr(value, "value"):
        value = value.value

    return str(value).strip().upper().replace("-", "_")


def customer_data(customer) -> dict:
    return {
        "customer_id": customer.id,
        "customer_code": customer.customer_code,
        "customer_fullname": customer.customer_fullname,
        "customer_email": customer.customer_email,
        "customer_phone": customer.customer_phone,
        "customer_full_address": customer.customer_full_address,
    }


def create_access_token(customer) -> str:
    header = {
        "typ": "JWT",
        "alg": "HS256",
    }
    payload = {
        "customer_id": customer.id,
        "customer_code": customer.customer_code,
        "customer_email": customer.customer_email,
        "exp": int(time.time()) + TOKEN_EXPIRE_SECONDS,
    }

    header_text = encode_base64_url(json.dumps(header, separators=(",", ":")).encode())
    payload_text = encode_base64_url(json.dumps(payload, separators=(",", ":")).encode())
    token_data = f"{header_text}.{payload_text}"
    signature = hmac.new(SECRET_KEY.encode(), token_data.encode(), sha256).digest()

    return f"{token_data}.{encode_base64_url(signature)}"


def encode_base64_url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def error_response(status_code: int, message: str):
    return JSONResponse(
        status_code=200,
        content={
            "success": False,
            "STATUS": "ERROR",
            "status_code": status_code,
            "message": message,
            "data": None,
            "access_token": None,
            "expire": None,
        },
    )
