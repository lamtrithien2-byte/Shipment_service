from sqlalchemy import Boolean, Column, Integer, String

from app.db.db_database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_code = Column(String(50), unique=True, nullable=False)
    customer_fullname = Column(String(255), nullable=False)
    customer_email = Column(String(255), unique=True, nullable=True)
    customer_phone = Column(String(30), unique=True, nullable=True)
    customer_full_address = Column(String(500), nullable=True)
    customer_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
