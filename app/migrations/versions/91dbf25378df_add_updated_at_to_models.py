"""add updated_at to entities and rooms models

Revision ID: 91dbf25378df
Revises: ddec4f5ded01
Create Date: 2022-11-27 15:37:54.213614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91dbf25378df'
down_revision = 'ddec4f5ded01'
branch_labels = None
depends_on = 'ddec4f5ded01'


def upgrade():
    op.add_column('entities', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('rooms', sa.Column('updated_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('rooms', 'updated_at')
    op.drop_column('entities', 'updated_at')
