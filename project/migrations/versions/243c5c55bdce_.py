"""empty message

Revision ID: 243c5c55bdce
Revises: ef986659abe7
Create Date: 2021-05-20 06:37:20.360684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '243c5c55bdce'
down_revision = 'ef986659abe7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('creation_dnt', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('activity_dnt', sa.DateTime(), nullable=True))
        batch_op.drop_column('dnt')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dnt', sa.DATETIME(), nullable=True))
        batch_op.drop_column('activity_dnt')
        batch_op.drop_column('creation_dnt')

    # ### end Alembic commands ###
