"""Add columns to user_activity

Revision ID: af014fbcffe9
Revises: 884dfcb3bd54
Create Date: 2024-12-01 11:15:30.353112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af014fbcffe9'
down_revision: Union[str, None] = '884dfcb3bd54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_activity', sa.Column('assistance', sa.Boolean(), nullable=True))
    op.add_column('user_activity', sa.Column('inserted', sa.DateTime(timezone=True), nullable=False))
    op.add_column('user_activity', sa.Column('updated', sa.DateTime(timezone=True), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_activity', 'updated')
    op.drop_column('user_activity', 'inserted')
    op.drop_column('user_activity', 'assistance')
    # ### end Alembic commands ###
