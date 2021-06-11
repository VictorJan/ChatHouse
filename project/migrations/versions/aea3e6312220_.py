"""empty message

Revision ID: aea3e6312220
Revises: fbf079c87566
Create Date: 2021-05-16 09:57:00.299893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aea3e6312220'
down_revision = 'fbf079c87566'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat', sa.Column('name', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'chat', ['name'])
    op.create_unique_constraint(None, 'keyring', ['public_key'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'keyring', type_='unique')
    op.drop_constraint(None, 'chat', type_='unique')
    op.drop_column('chat', 'name')
    # ### end Alembic commands ###