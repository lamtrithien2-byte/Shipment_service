"""create customers

Revision ID: 001_create_customers
Revises:
Create Date: 2026-05-07
"""

from alembic import op
import sqlalchemy as sa

revision = "001_create_customers"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_code", sa.String(length=50), nullable=False),
        sa.Column("customer_fullname", sa.String(length=255), nullable=False),
        sa.Column("customer_email", sa.String(length=255), nullable=True),
        sa.Column("customer_phone", sa.String(length=30), nullable=True),
        sa.Column("customer_full_address", sa.String(length=500), nullable=True),
        sa.Column("customer_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("customer_code"),
        sa.UniqueConstraint("customer_email"),
        sa.UniqueConstraint("customer_phone"),
    )
    op.create_index("ix_customers_id", "customers", ["id"])


def downgrade():
    op.drop_index("ix_customers_id", table_name="customers")
    op.drop_table("customers")
