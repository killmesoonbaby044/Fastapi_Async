"""test_column_add

Revision ID: 0ebb3da59d70
Revises: 
Create Date: 2024-04-16 09:31:42.087415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ebb3da59d70'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("test1",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("name", sa.String, nullable=False),
                    sa.Column("description", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("test1")
    pass
