"""delete refresh_tokens table

Revision ID: 193d86216bb1
Revises: 157a9bac82b9
Create Date: 2021-09-26 16:54:21.061511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '193d86216bb1'
down_revision = '157a9bac82b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('refresh_tokens')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('refresh_tokens',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('account_id', sa.INTEGER(), nullable=False),
        sa.Column('token', sa.VARCHAR(), nullable=False),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('account_id')
    )
    # ### end Alembic commands ###
