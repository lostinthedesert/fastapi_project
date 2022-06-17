"""create post table

Revision ID: b4a944c50e7e
Revises: 
Create Date: 2022-06-15 14:38:17.313983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4a944c50e7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True), sa.Column('title', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
