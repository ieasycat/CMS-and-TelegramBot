"""empty message

Revision ID: 35354d49501d
Revises: 53c217f0c2b3
Create Date: 2022-06-15 11:35:57.454832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35354d49501d'
down_revision = '53c217f0c2b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('main_technology', sa.String(length=50), nullable=True))
    op.add_column('employee', sa.Column('status', sa.String(length=15), nullable=True))
    op.drop_column('employee_data', 'main_technology')
    op.drop_column('employee_data', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee_data', sa.Column('status', sa.VARCHAR(length=15), autoincrement=False, nullable=True))
    op.add_column('employee_data', sa.Column('main_technology', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('employee', 'status')
    op.drop_column('employee', 'main_technology')
    # ### end Alembic commands ###