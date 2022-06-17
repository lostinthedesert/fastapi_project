"""create users table

Revision ID: 810e5d5c476b
Revises: 39eb7a2873f1
Create Date: 2022-06-15 17:27:52.412103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '810e5d5c476b'
down_revision = '39eb7a2873f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('email', sa.String, nullable=False),
                    sa.Column('password',sa.String, nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
