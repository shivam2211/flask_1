"""new fields in user model

Revision ID: cc9945c8c57b
Revises: 9f26c8a7fbae
Create Date: 2019-08-08 13:16:47.263184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc9945c8c57b'
down_revision = '9f26c8a7fbae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
