"""test

Revision ID: d03f00ab0f06
Revises: 7dd4aa704c76
Create Date: 2024-04-16 12:25:47.320220

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd03f00ab0f06'
down_revision: Union[str, None] = '7dd4aa704c76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
