"""add task status

Revision ID: c17130c9f8c4
Revises: 7b480c261978
Create Date: 2022-09-29 16:47:13.456486

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'c17130c9f8c4'
down_revision = '7b480c261978'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('status', sa.Enum('OPEN', 'COMPLETE', name='taskstatus'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'status')
    # ### end Alembic commands ###
