"""empty message

Revision ID: 5de70af99d6d
Revises: a5cffa318ac2
Create Date: 2023-11-24 01:52:50.532581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5de70af99d6d'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('mass', sa.Integer(), nullable=False),
    sa.Column('hair_color', sa.String(length=120), nullable=False),
    sa.Column('skin_color', sa.String(length=120), nullable=False),
    sa.Column('eye_color', sa.String(length=120), nullable=False),
    sa.Column('favorite_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['favorite_id'], ['favorite.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('eye_color'),
    sa.UniqueConstraint('hair_color'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('skin_color')
    )
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('rotation_period', sa.Integer(), nullable=False),
    sa.Column('orbital_period', sa.Integer(), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=False),
    sa.Column('climate', sa.String(length=120), nullable=False),
    sa.Column('graviti', sa.Integer(), nullable=False),
    sa.Column('favorite_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['favorite_id'], ['favorite.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('phone', sa.Integer(), nullable=False))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=80),
               type_=sa.String(length=30),
               existing_nullable=False)
        batch_op.drop_constraint('user_email_key', type_='unique')
        batch_op.create_unique_constraint(None, ['password'])
        batch_op.create_unique_constraint(None, ['name'])
        batch_op.create_unique_constraint(None, ['phone'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint('user_email_key', ['email'])
        batch_op.alter_column('password',
               existing_type=sa.String(length=30),
               type_=sa.VARCHAR(length=80),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.drop_column('phone')
        batch_op.drop_column('name')

    op.drop_table('planet')
    op.drop_table('people')
    op.drop_table('favorite')
    # ### end Alembic commands ###
