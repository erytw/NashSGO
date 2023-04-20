"""add new table

Revision ID: b52164d20ace
Revises: 56df5c6b0df6
Create Date: 2023-04-18 02:13:03.271206

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b52164d20ace'
down_revision = '56df5c6b0df6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sgo_users',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('tg_id', sa.Integer(), nullable=False),
        sa.Column('login', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('school', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tg_id')
    )


def downgrade():
    op.drop_table('sgo_users')
