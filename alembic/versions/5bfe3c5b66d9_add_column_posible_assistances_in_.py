"""Add column posible assistances in Activity

Revision ID: 5bfe3c5b66d9
Revises: af014fbcffe9
Create Date: 2024-12-04 08:07:21.166543

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bfe3c5b66d9'
down_revision: Union[str, None] = 'af014fbcffe9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activity', sa.Column('number_of_possible_assistances', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('activity', 'number_of_possible_assistances')
    # ### end Alembic commands ###
