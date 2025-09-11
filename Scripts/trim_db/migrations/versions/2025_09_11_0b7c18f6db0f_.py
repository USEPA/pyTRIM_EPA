"""
Model run updates

Revision ID: 0b7c18f6db0f
Revises: 60eb40203023
Create Date: 2025-09-11 07:27:43.458337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b7c18f6db0f'
down_revision = '60eb40203023'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "ALTER TABLE scenario_load_run_proc ADD COLUMN execution_arn VARCHAR(255);"
    )


def downgrade():
    op.execute(
        "ALTER TABLE scenario_load_run_proc DROP COLUMN execution_arn;"
    )
