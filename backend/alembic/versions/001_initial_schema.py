"""Initial schema with classifications, feedback, and daily_metrics tables

Revision ID: 001
Revises: 
Create Date: 2024-12-12

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema."""
    
    # Create classifications table
    op.create_table(
        'classifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('classification', sa.String(length=10), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('model_version', sa.String(length=50), nullable=True),
        sa.Column('image_quality_score', sa.Float(), nullable=True),
        sa.Column('image_width', sa.Integer(), nullable=True),
        sa.Column('image_height', sa.Integer(), nullable=True),
        sa.Column('image_format', sa.String(length=10), nullable=True),
        sa.Column('image_size_bytes', sa.Integer(), nullable=True),
        sa.Column('has_glare', sa.Boolean(), nullable=True),
        sa.Column('preprocessing_applied', sa.JSON(), nullable=True),
        sa.Column('product_category', sa.String(length=100), nullable=True),
        sa.Column('feature_scores', sa.JSON(), nullable=True),
        sa.Column('textual_reasons', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_classifications_id'), 'classifications', ['id'], unique=False)
    op.create_index(op.f('ix_classifications_request_id'), 'classifications', ['request_id'], unique=True)
    op.create_index(op.f('ix_classifications_timestamp'), 'classifications', ['timestamp'], unique=False)
    
    # Create feedback table
    op.create_table(
        'feedback',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('feedback_type', sa.String(length=20), nullable=False),
        sa.Column('user_comments', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('flagged_for_review', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['request_id'], ['classifications.request_id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feedback_id'), 'feedback', ['id'], unique=False)
    op.create_index(op.f('ix_feedback_request_id'), 'feedback', ['request_id'], unique=False)
    op.create_index(op.f('ix_feedback_timestamp'), 'feedback', ['timestamp'], unique=False)
    op.create_index(op.f('ix_feedback_flagged_for_review'), 'feedback', ['flagged_for_review'], unique=False)
    
    # Create daily_metrics table
    op.create_table(
        'daily_metrics',
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('total_classifications', sa.Integer(), nullable=False),
        sa.Column('avg_confidence', sa.Float(), nullable=True),
        sa.Column('correct_feedback_count', sa.Integer(), nullable=True),
        sa.Column('incorrect_feedback_count', sa.Integer(), nullable=True),
        sa.Column('avg_processing_time_ms', sa.Float(), nullable=True),
        sa.Column('category_distribution', sa.JSON(), nullable=True),
        sa.Column('classification_distribution', sa.JSON(), nullable=True),
        sa.Column('low_confidence_count', sa.Integer(), nullable=True),
        sa.Column('medium_confidence_count', sa.Integer(), nullable=True),
        sa.Column('high_confidence_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('date')
    )
    op.create_index(op.f('ix_daily_metrics_date'), 'daily_metrics', ['date'], unique=False)


def downgrade() -> None:
    """Drop all tables."""
    op.drop_index(op.f('ix_daily_metrics_date'), table_name='daily_metrics')
    op.drop_table('daily_metrics')
    
    op.drop_index(op.f('ix_feedback_flagged_for_review'), table_name='feedback')
    op.drop_index(op.f('ix_feedback_timestamp'), table_name='feedback')
    op.drop_index(op.f('ix_feedback_request_id'), table_name='feedback')
    op.drop_index(op.f('ix_feedback_id'), table_name='feedback')
    op.drop_table('feedback')
    
    op.drop_index(op.f('ix_classifications_timestamp'), table_name='classifications')
    op.drop_index(op.f('ix_classifications_request_id'), table_name='classifications')
    op.drop_index(op.f('ix_classifications_id'), table_name='classifications')
    op.drop_table('classifications')
