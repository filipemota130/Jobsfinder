"""empty message

Revision ID: d37361e3db8a
Revises: 
Create Date: 2021-03-20 17:34:15.168568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd37361e3db8a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nick_name', sa.String(length=80), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('number', sa.String(length=16), nullable=False),
    sa.Column('date', sa.String(length=10), nullable=False),
    sa.Column('desc', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('nick_name')
    )
    op.create_table('jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('category', sa.String(length=80), nullable=False),
    sa.Column('valor', sa.String(), nullable=False),
    sa.Column('desc', sa.String(), nullable=False),
    sa.Column('outros', sa.String(), nullable=True),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('name_user', sa.String(), nullable=True),
    sa.Column('identifier', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.ForeignKeyConstraint(['name_user'], ['users.nick_name'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('identifier')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('jobs')
    op.drop_table('users')
    # ### end Alembic commands ###