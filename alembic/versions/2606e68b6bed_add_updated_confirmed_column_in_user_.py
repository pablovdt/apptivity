"""Add updated_confirmed column in user_activity

Revision ID: 2606e68b6bed
Revises: e227d530db67
Create Date: 2024-12-07 10:28:41.397524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2606e68b6bed'
down_revision: Union[str, None] = 'e227d530db67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_activity', sa.Column('updated_confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_activity', 'updated_confirmed')
    # ### end Alembic commands ###