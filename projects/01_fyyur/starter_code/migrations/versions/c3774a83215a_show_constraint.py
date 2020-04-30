"""show constraint

Revision ID: c3774a83215a
Revises: bab5b6cfa48b
Create Date: 2020-05-01 01:19:58.476276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3774a83215a'
down_revision = 'bab5b6cfa48b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('same_artist_start_time', 'Shows', ['artist_id', 'start_time'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('same_artist_start_time', 'Shows', type_='unique')
    # ### end Alembic commands ###