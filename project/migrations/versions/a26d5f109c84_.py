"""empty message

Revision ID: a26d5f109c84
Revises: 228b069c93a3
Create Date: 2021-05-17 17:28:01.927206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a26d5f109c84'
down_revision = '228b069c93a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about', sa.String(), nullable=False))
        batch_op.alter_column('token_version',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('token_version',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.drop_column('about')

    # ### end Alembic commands ###
