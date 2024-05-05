"""insert base withdrawl methods data

Revision ID: 28c2da5f36b7
Revises: 7fb4910067f3
Create Date: 2024-05-01 20:15:47.510860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28c2da5f36b7'
down_revision: Union[str, None] = '7fb4910067f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    meta = sa.MetaData()

    meta.reflect(only=('withdrawal_methods', ), bind=op.get_bind())

    withdrawal_statuses_table = sa.Table('withdrawal_methods', meta)

    op.bulk_insert(
        withdrawal_statuses_table,
        [
            {
                "name": "CRYPTO",
                "slug_name": "crypto",
            },
            {
                "name": "FIAT",
                "slug_name": "fiat"
            }
        ]
    )


def downgrade() -> None:
    pass
