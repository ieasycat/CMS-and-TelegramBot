"""empty message

Revision ID: 16a874f45792
Revises: ee991f75d522
Create Date: 2022-07-05 16:44:08.687770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16a874f45792'
down_revision = 'ee991f75d522'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('manager', sa.Column('token', sa.String(length=32), nullable=True))
    op.create_index(op.f('ix_manager_token'), 'manager', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_manager_token'), table_name='manager')
    op.drop_column('manager', 'token')
    # ### end Alembic commands ###
