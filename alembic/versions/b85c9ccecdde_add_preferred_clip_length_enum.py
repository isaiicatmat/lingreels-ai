"""Add preferred_clip_length enum

Revision ID: b85c9ccecdde
Revises: a6860ae739ff
Create Date: 2025-03-18 11:19:29.526146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b85c9ccecdde'
down_revision: Union[str, None] = 'a6860ae739ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('clips', 'start_time',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('clips', 'end_time',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)
    op.alter_column('clips', 'preferred_clip_length',
               existing_type=postgresql.ENUM('short', 'medium', 'long', name='cliplengthenum'),
               type_=sa.Enum('SHORT', 'MEDIUM', 'LONG', name='cliplengthenum', native_enum=False),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('clips', 'preferred_clip_length',
               existing_type=sa.Enum('SHORT', 'MEDIUM', 'LONG', name='cliplengthenum', native_enum=False),
               type_=postgresql.ENUM('short', 'medium', 'long', name='cliplengthenum'),
               existing_nullable=True)
    op.alter_column('clips', 'end_time',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('clips', 'start_time',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###
