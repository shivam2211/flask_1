"""add language to posts

Revision ID: 9f26c8a7fbae
Revises: 6dcc3fec26a4
Create Date: 2019-08-08 10:40:49.308684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f26c8a7fbae'
down_revision = '6dcc3fec26a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'language')
    # ### end Alembic commands ###
