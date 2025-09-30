"""
Flush rate autocalculate
Erosion param cleanup

Revision ID: 90beadf3f7d6
Revises: 81e92f9ff252
Create Date: 2025-09-28 14:06:28.433082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90beadf3f7d6'
down_revision = '81e92f9ff252'
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

    op.execute(
        """
        DELETE FROM custom_parameter WHERE unit IS NOT NULL AND definition_id IN (
            SELECT id FROM parameter_definition WHERE variable_name LIKE 'erosion%'
        );
        """
    )


def downgrade():
    pass
