"""Initial migration

Revision ID: 790e6a06828c
Revises: 
Create Date: 2025-03-17 17:31:14.235755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '790e6a06828c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('video_url', sa.String(length=255), nullable=False),
    sa.Column('video_length', sa.Integer(), nullable=True),
    sa.Column('uploaded_at', sa.DateTime(), nullable=True),
    sa.Column('processed', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_videos_id'), 'videos', ['id'], unique=False)
    op.create_table('ai_processing_queue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.Integer(), nullable=True),
    sa.Column('task_name', sa.String(length=100), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('started_at', sa.DateTime(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_processing_queue_id'), 'ai_processing_queue', ['id'], unique=False)
    op.create_table('clips',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.Integer(), nullable=True),
    sa.Column('end_time', sa.Integer(), nullable=True),
    sa.Column('clip_url', sa.String(length=255), nullable=True),
    sa.Column('engagement_score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clips_id'), 'clips', ['id'], unique=False)
    op.create_table('highlights',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.Integer(), nullable=True),
    sa.Column('end_time', sa.Integer(), nullable=True),
    sa.Column('highlight_score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_highlights_id'), 'highlights', ['id'], unique=False)
    op.create_table('captions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('clip_id', sa.Integer(), nullable=True),
    sa.Column('language', sa.String(length=10), nullable=True),
    sa.Column('caption_text', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['clip_id'], ['clips.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_captions_id'), 'captions', ['id'], unique=False)
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('clip_id', sa.Integer(), nullable=True),
    sa.Column('tag', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['clip_id'], ['clips.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tags_id'), 'tags', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tags_id'), table_name='tags')
    op.drop_table('tags')
    op.drop_index(op.f('ix_captions_id'), table_name='captions')
    op.drop_table('captions')
    op.drop_index(op.f('ix_highlights_id'), table_name='highlights')
    op.drop_table('highlights')
    op.drop_index(op.f('ix_clips_id'), table_name='clips')
    op.drop_table('clips')
    op.drop_index(op.f('ix_ai_processing_queue_id'), table_name='ai_processing_queue')
    op.drop_table('ai_processing_queue')
    op.drop_index(op.f('ix_videos_id'), table_name='videos')
    op.drop_table('videos')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
