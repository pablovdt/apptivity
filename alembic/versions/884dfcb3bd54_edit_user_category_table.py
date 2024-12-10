"""edit user_category table

Revision ID: 884dfcb3bd54
Revises: 58e5def3daba
Create Date: 2024-11-30 11:57:44.240652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '884dfcb3bd54'
down_revision: Union[str, None] = '58e5def3daba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('user_category', 'user_id',
                    existing_type=sa.INTEGER(),
                    nullable=False)
    op.alter_column('user_category', 'category_id',
                    existing_type=sa.INTEGER(),
                    nullable=False)

    op.create_primary_key(
        'pk_user_category',
        'user_category',
        ['user_id', 'category_id']
    )


def downgrade() -> None:
    op.drop_constraint('pk_user_category', 'user_category', type_='primary')

    op.alter_column('user_category', 'category_id',
                    existing_type=sa.INTEGER(),
                    nullable=True)
    op.alter_column('user_category', 'user_id',
                    existing_type=sa.INTEGER(),
                    nullable=True)
