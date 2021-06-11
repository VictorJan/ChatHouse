"""empty message

Revision ID: 2191ccbca41d
Revises: e47f1b4b1cfa
Create Date: 2021-05-16 10:27:13.449788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2191ccbca41d'
down_revision = 'e47f1b4b1cfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))
        batch_op.create_unique_constraint(batch_op.f('uq_chat_name'), ['name'])

    with op.batch_alter_table('keyring', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_keyring_owner_id'), ['owner_id', 'public_key', 'private_key'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_username'), ['username', 'email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_username'), type_='unique')

    with op.batch_alter_table('keyring', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_keyring_owner_id'), type_='unique')

    with op.batch_alter_table('chat', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_chat_name'), type_='unique')
        batch_op.drop_column('name')

    # ### end Alembic commands ###