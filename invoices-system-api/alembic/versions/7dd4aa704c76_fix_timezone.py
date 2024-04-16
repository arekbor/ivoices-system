"""Fix timezone

Revision ID: 7dd4aa704c76
Revises: 9886823b7356
Create Date: 2024-04-16 12:04:08.612708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dd4aa704c76'
down_revision: Union[str, None] = '9886823b7356'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
