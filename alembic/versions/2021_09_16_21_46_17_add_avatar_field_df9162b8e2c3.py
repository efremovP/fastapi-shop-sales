"""add 'avatar' field

Revision ID: df9162b8e2c3
Revises: fb027df22c8f
Create Date: 2021-09-16 21:46:17.750718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df9162b8e2c3'
down_revision = 'fb027df22c8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('avatar', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'avatar')
    # ### end Alembic commands ###