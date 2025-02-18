"""add_movie_actors_table

Revision ID: 26650479f646
Revises: 4f673c4ded31
Create Date: 2025-02-17 03:02:58.000925+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26650479f646'
down_revision: Union[str, None] = '4f673c4ded31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movie_actors',
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.actor_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.movie_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('movie_id', 'actor_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie_actors')
    # ### end Alembic commands ###
