"""empty message

Revision ID: 163da8e4bce7
Revises: 6585dccd1e72
Create Date: 2022-07-14 16:11:58.926684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '163da8e4bce7'
down_revision = '6585dccd1e72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_url', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_url')
    # ### end Alembic commands ###
