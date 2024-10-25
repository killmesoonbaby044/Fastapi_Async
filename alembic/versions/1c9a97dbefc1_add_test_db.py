"""add test db

Revision ID: 1c9a97dbefc1
Revises: 622cf159740f
Create Date: 2024-04-24 19:23:44.375342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c9a97dbefc1'
down_revision: Union[str, None] = '622cf159740f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.cre


def downgrade() -> None:
    pass
