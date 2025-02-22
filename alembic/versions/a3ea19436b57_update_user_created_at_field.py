"""update user created_at field

Revision ID: a3ea19436b57
Revises: 0d8c4bb92d47
Create Date: 2025-01-13 06:42:59.371208+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3ea19436b57'
down_revision: Union[str, None] = '0d8c4bb92d47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'created_at')
    # ### end Alembic commands ###