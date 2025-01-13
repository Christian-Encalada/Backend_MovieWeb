"""update_favs_to_json

Revision ID: xxxx
Revises: 90d0359104d2
Create Date: 2024-01-14 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = 'xxxx'
down_revision: Union[str, None] = '90d0359104d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Primero, asegurarnos de que los valores nulos se conviertan a lista vacía
    op.execute("""
        UPDATE users 
        SET favs = '[]'::jsonb 
        WHERE favs IS NULL;
    """)
    
    # Luego, convertir la columna a JSONB si no es del tipo correcto
    op.execute("""
        ALTER TABLE users 
        ALTER COLUMN favs TYPE jsonb USING 
        CASE 
            WHEN favs IS NULL THEN '[]'::jsonb
            WHEN jsonb_typeof(favs::jsonb) = 'array' THEN favs::jsonb
            ELSE '[]'::jsonb
        END;
    """)
    
    # Establecer el valor por defecto
    op.alter_column('users', 'favs',
        type_=JSONB,
        nullable=True,
        server_default=sa.text("'[]'::jsonb")
    )

def downgrade() -> None:
    # En caso de necesitar revertir, volvemos a JSON
    op.alter_column('users', 'favs',
        type_=sa.JSON,
        nullable=True,
        server_default=None
    ) 