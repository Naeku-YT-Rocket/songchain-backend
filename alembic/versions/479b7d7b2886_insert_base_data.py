"""insert base data

Revision ID: 479b7d7b2886
Revises: ecfdb68e02f2
Create Date: 2024-04-12 11:36:28.748400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '479b7d7b2886'
down_revision: Union[str, None] = 'ecfdb68e02f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  
    meta = sa.MetaData()

    meta.reflect(only=('withdrawal_statuses', ), bind=op.get_bind())

    withdrawal_statuses_table = sa.Table('withdrawal_statuses', meta)

    op.bulk_insert(
        withdrawal_statuses_table,
        [
            {
                "name": "CANCELLED",
                "slug_name": "cancelled",
                "description": "Cancelled status"
            },
            {
                "name": "REQUESTED",
                "slug_name": "requested",
                "description": "Requested status"
            },
            {
                "name": "PAID",
                "slug_name": "paid",
                "description": "paid status"
            },
            {
                "name": "REJECTED",
                "slug_name": "rejected",
                "description": "Rejected status"
            }
        ]
    )

    meta.reflect(only=('partition_statuses', ), bind=op.get_bind())

    partition_statuses_table = sa.Table('partition_statuses', meta)

    op.bulk_insert(
        partition_statuses_table,
        [
            {
                "name": "OFFERED",
                "slug_name": "offered",
                "description": "Offered status"
            },
            {
                "name": "CANCELLED",
                "slug_name": "cancelled",
                "description": "Cancelled status"
            },
            {
                "name": "PURCHASED",
                "slug_name": "purchased",
                "description": "Purchased status"
            }
        ]
    )



def downgrade() -> None:
    pass
