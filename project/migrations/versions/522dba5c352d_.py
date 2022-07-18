"""empty message

Revision ID: 522dba5c352d
Revises: 0aa375b934cd
Create Date: 2021-05-16 10:08:25.008900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '522dba5c352d'
down_revision = '0aa375b934cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('keyring', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['public_key'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('keyring', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###