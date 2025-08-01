"""CollectionChatHistory update

Revision ID: 9c2745e14cf3
Revises: 3ed502b73c2d
Create Date: 2025-07-24 09:40:50.044985

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9c2745e14cf3"
down_revision: Union[str, Sequence[str], None] = "3ed502b73c2d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "collection_chat_history",
        sa.Column(
            "role",
            sa.Enum("user", "assistant", "system", name="role", native_enum=False),
            nullable=False,
        ),
    )
    op.add_column(
        "collection_chat_history", sa.Column("content", sa.Text(), nullable=False)
    )
    op.drop_column("collection_chat_history", "text")
    op.drop_column("collection_chat_history", "instruct")
    op.drop_column("collection_chat_history", "system_prompt")
    op.drop_column("collection_chat_history", "agent")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "collection_chat_history",
        sa.Column("agent", sa.TEXT(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "collection_chat_history",
        sa.Column("system_prompt", sa.TEXT(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "collection_chat_history",
        sa.Column("instruct", sa.TEXT(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "collection_chat_history",
        sa.Column("text", sa.TEXT(), autoincrement=False, nullable=False),
    )
    op.drop_column("collection_chat_history", "content")
    op.drop_column("collection_chat_history", "role")
    # ### end Alembic commands ###
