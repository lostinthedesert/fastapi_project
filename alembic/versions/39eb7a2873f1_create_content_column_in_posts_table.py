"""create content column in posts table

Revision ID: 39eb7a2873f1
Revises: b4a944c50e7e
Create Date: 2022-06-15 17:09:29.514027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39eb7a2873f1'
down_revision = 'b4a944c50e7e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa. String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
