"""
Farm media
AverageVerticalVelocity

Revision ID: 60eb40203023
Revises: 151911e8b6a9
Create Date: 2025-08-15 13:38:00.664906

"""
from alembic import op
import sqlalchemy as sa
from trim_db.migrations.utils import has_results


# revision identifiers, used by Alembic.
revision = '60eb40203023'
down_revision = '151911e8b6a9'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "UPDATE media SET parent_id = 34 WHERE name='Farm'"
    )

    # AverageVerticalVelocity = 0.2 * precip
    # where default value of Rain = 0.0041
    if not has_results("SELECT * FROM formula WHERE equation = '0.2 * environment.Rain' AND description= 'default AverageVerticalVelocity'"):
        op.execute(
            "INSERT INTO formula (equation, description) VALUES ('0.2 * environment.Rain', 'default AverageVerticalVelocity');"
        )
    op.execute(
        """
        UPDATE parameter_definition
        SET default_value = 0.00082,
        default_formula_id = (
            SELECT id FROM formula
            WHERE equation = '0.2 * environment.Rain' AND description= 'default AverageVerticalVelocity'
        ) WHERE variable_name = 'AverageVerticalVelocity';
        """
    )



def downgrade():
    op.execute(
        "UPDATE media SET parent_id = NULL WHERE name='Farm'"
    )

    op.execute(
        "UPDATE parameter_definition SET default_value = 0.0006, default_formula_id = NULL WHERE variable_name = 'AverageVerticalVelocity';"
    )

    op.execute(
        "DELETE FROM formula WHERE equation = '0.2 * environment.Rain' AND description= 'default AverageVerticalVelocity';"
    )

    #op.execute(
    #    """
    #    DELETE FROM parameter_definition WHERE variable_name = 'mixingHeight' AND domain_id = 1;
    #    """
    #)
