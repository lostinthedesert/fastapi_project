# THIS REVISION DID NOT WORK AND A DUPLICATE WAS CREATED TO SKIP IT


"""add remaining posts columns

Revision ID: f68a733e24e0
Revises: 7563ce1ecd9e
Create Date: 2022-06-15 17:55:47.608610

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f68a733e24e0'
down_revision = '7563ce1ecd9e'
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
