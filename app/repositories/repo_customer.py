from sqlalchemy.orm import Session

from app.models.model_customer import Customer


def get_customer_by_email(db: Session, email: str) -> Customer | None:
    return db.query(Customer).filter(Customer.customer_email == email).first()


def get_customer_by_mobile(db: Session, mobile: str) -> Customer | None:
    return db.query(Customer).filter(Customer.customer_phone == mobile).first()


def get_login_customer(db: Session, email: str | None, mobile: str | None) -> Customer | None:
    if email:
        return get_customer_by_email(db, email)

    if mobile:
        return get_customer_by_mobile(db, mobile)

    return None
