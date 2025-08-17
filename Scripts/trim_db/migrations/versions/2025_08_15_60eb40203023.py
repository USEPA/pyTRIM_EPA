"""
Farm media

Revision ID: 60eb40203023
Revises: 151911e8b6a9
Create Date: 2025-08-15 13:38:00.664906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60eb40203023'
down_revision = '151911e8b6a9'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "UPDATE media SET parent_id = 34 WHERE name='Farm'"
    )


def downgrade():
    op.execute(
        "UPDATE media SET parent_id = NULL WHERE name='Farm'"
    )
