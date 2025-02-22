"""add_tmdb_and_user_genres

Revision ID: 48e28df98afc
Revises: e1d715b67bd8
Create Date: 2025-02-17 02:58:32.474099+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48e28df98afc'
down_revision: Union[str, None] = 'e1d715b67bd8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('tmdb_id', sa.Integer(), nullable=True))
    op.add_column('movies', sa.Column('poster_path', sa.String(), nullable=True))
    op.add_column('movies', sa.Column('overview', sa.Text(), nullable=True))
    op.add_column('movies', sa.Column('release_date', sa.Date(), nullable=True))
    op.add_column('movies', sa.Column('vote_average', sa.Float(), nullable=True))
    op.add_column('movies', sa.Column('vote_count', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'movies', ['tmdb_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'movies', type_='unique')
    op.drop_column('movies', 'vote_count')
    op.drop_column('movies', 'vote_average')
    op.drop_column('movies', 'release_date')
    op.drop_column('movies', 'overview')
    op.drop_column('movies', 'poster_path')
    op.drop_column('movies', 'tmdb_id')
    # ### end Alembic commands ###
