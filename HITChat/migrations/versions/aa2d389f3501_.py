"""empty message

Revision ID: aa2d389f3501
Revises: 
Create Date: 2017-11-11 11:35:42.440943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa2d389f3501'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('top',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'user', sa.Column('isAdmin', sa.Integer(), nullable=True))
    op.add_column(u'user', sa.Column('picid', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'user', 'picid')
    op.drop_column(u'user', 'isAdmin')
    op.drop_table('top')
    # ### end Alembic commands ###
