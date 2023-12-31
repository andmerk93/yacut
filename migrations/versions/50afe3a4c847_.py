"""empty message

Revision ID: 50afe3a4c847
Revises: 6fb1c2a2c318
Create Date: 2023-07-23 04:47:44.609606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50afe3a4c847'
down_revision = '6fb1c2a2c318'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('url_map', sa.Column('original', sa.String(length=256), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('url_map', sa.Column('original', sa.String(), nullable=False))
    # ### end Alembic commands ###
