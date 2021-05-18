"""empty message

Revision ID: fbf079c87566
Revises: fd832688fd28
Create Date: 2021-05-16 07:50:42.816520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbf079c87566'
down_revision = 'fd832688fd28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'keyring', ['public_key'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'keyring', type_='unique')
    # ### end Alembic commands ###