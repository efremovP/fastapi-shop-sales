"""remove first_name, last_name,avatar from accounts table

Revision ID: 157a9bac82b9
Revises: 200e5d6a163d
Create Date: 2021-09-24 13:17:41.769254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '157a9bac82b9'
down_revision = '200e5d6a163d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('accounts', 'last_name')
    op.drop_column('accounts', 'first_name')
    op.drop_column('accounts', 'avatar')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('avatar', sa.VARCHAR(), nullable=True))
    op.add_column('accounts', sa.Column('first_name', sa.VARCHAR(), nullable=True))
    op.add_column('accounts', sa.Column('last_name', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###
