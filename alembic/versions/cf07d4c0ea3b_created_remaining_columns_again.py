"""created remaining columns again

Revision ID: cf07d4c0ea3b
Revises: f68a733e24e0
Create Date: 2022-06-15 18:18:49.908565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf07d4c0ea3b'
down_revision = 'f68a733e24e0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),)
    op.add_column('posts', sa.Column('published', sa.Boolean, server_default='TRUE', nullable=False),)
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass

