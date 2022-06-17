"""create foreign key owner_id

Revision ID: 7563ce1ecd9e
Revises: 810e5d5c476b
Create Date: 2022-06-15 17:42:38.078034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7563ce1ecd9e'
down_revision = '810e5d5c476b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id',sa.Integer, nullable=False)),
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users',local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', 'posts')
    op.drop_column('posts', 'owner_id')
    pass
