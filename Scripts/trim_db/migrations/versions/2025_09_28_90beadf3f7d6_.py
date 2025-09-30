"""
Flush rate autocalculate

Revision ID: 90beadf3f7d6
Revises: 287d3ddae792
Create Date: 2025-09-28 14:06:28.433082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90beadf3f7d6'
down_revision = '287d3ddae792'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        INSERT INTO formula (equation, description) 
        VALUES ('True', 'flush rate is autocalculated');
        """
    )
    op.execute(
        """
        UPDATE parameter_definition
        SET default_formula_id = (
            SELECT id FROM formula
            WHERE description= 'flush rate is autocalculated'
        ) WHERE variable_name = 'Flushes';
        """
    )


def downgrade():
    pass
