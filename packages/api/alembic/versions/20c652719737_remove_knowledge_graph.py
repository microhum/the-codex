"""remove knowledge graph

Revision ID: 20c652719737
Revises: d3039163db09
Create Date: 2025-07-02 23:46:19.747685

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20c652719737"
down_revision: Union[str, Sequence[str], None] = "d3039163db09"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("document", "knowledge_graph")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "document",
        sa.Column(
            "knowledge_graph",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    # ### end Alembic commands ###
