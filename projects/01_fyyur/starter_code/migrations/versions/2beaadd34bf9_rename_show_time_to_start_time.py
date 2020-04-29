"""rename show_time to start_time

Revision ID: 2beaadd34bf9
Revises: 41eacd9a7556
Create Date: 2020-04-29 00:06:56.922691

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2beaadd34bf9'
down_revision = '41eacd9a7556'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Artists', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=False)
    op.add_column('Shows', sa.Column('start_time', sa.DateTime(), nullable=True))
    op.drop_column('Shows', 'show_time')
    op.alter_column('Venues', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venues', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=True)
    op.add_column('Shows', sa.Column('show_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('Shows', 'start_time')
    op.alter_column('Artists', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=True)
    # ### end Alembic commands ###