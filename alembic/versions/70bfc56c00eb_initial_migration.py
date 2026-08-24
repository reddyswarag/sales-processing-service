"""initial migration

Revision ID: 70bfc56c00eb
Revises:
Create Date: 2026-08-21 16:29:56.376762
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "70bfc56c00eb"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the initial jobs table."""

    op.create_table(
        "jobs",

        sa.Column(
            "job_id",
            sa.Integer(),
            sa.Identity(always=True),
            primary_key=True
        ),

        sa.Column(
            "task",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "status",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "file_path",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "result",
            postgresql.JSONB(),
            nullable=True
        ),

        sa.Column(
            "error",
            sa.Text(),
            nullable=True
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False
        ),

        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=True
        ),

        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True
        ),

        sa.Column(
            "current_attempt",
            sa.Integer(),
            server_default="0",
            nullable=False
        ),

        sa.Column(
            "max_attempts",
            sa.Integer(),
            server_default="3",
            nullable=False
        )
    )


def downgrade() -> None:
    """Remove the jobs table."""

    op.drop_table("jobs")