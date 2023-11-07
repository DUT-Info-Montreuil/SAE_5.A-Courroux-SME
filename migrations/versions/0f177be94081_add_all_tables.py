"""Add all tables

Revision ID: 0f177be94081
Revises: ee387158c374
Create Date: 2023-10-16 15:36:45.396171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f177be94081'
down_revision = 'ee387158c374'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cours', schema=None) as batch_op:
        batch_op.add_column(sa.Column('enseignant', sa.String(length=15), nullable=True))
        batch_op.add_column(sa.Column('ressource', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('promotion', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('groupe', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('salle', sa.String(length=64), nullable=True))
        batch_op.create_foreign_key(None, 'ressources', ['ressource'], ['name'])
        batch_op.create_foreign_key(None, 'enseignant', ['enseignant'], ['initial'])
        batch_op.create_foreign_key(None, 'promotion', ['promotion'], ['name'])
        batch_op.create_foreign_key(None, 'groupe', ['groupe'], ['idGroupe'])
        batch_op.create_foreign_key(None, 'salle', ['salle'], ['nom'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cours', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('salle')
        batch_op.drop_column('groupe')
        batch_op.drop_column('promotion')
        batch_op.drop_column('ressource')
        batch_op.drop_column('enseignant')

    # ### end Alembic commands ###
