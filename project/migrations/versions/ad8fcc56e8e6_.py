"""empty message

Revision ID: ad8fcc56e8e6
Revises: 86f11f2ecba3
Create Date: 2021-05-14 13:15:00.679747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad8fcc56e8e6'
down_revision = '86f11f2ecba3'
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
