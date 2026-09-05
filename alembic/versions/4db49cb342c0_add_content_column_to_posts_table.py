"""add content column to posts table

Revision ID: 4db49cb342c0
Revises: 9cd3564b7d45
Create Date: 2026-09-05 23:02:04.873863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4db49cb342c0'
down_revision: Union[str, Sequence[str], None] = '9cd3564b7d45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
