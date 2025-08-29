"""
Farm media
mixingHeight
AverageVerticalVelocity

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

    # default value of Rain = 0.0041 * 0.2
    op.execute(
        "UPDATE parameter_definition SET default_value = 0.00082 WHERE variable_name = 'AverageVerticalVelocity';"
    )

    #op.execute(
    #    """
    #    INSERT INTO parameter_definition (variable_name, full_name, domain_id, default_unit, default_value)
    #    VALUES ('mixingHeight', 'mixingHeight', 1, 'm', 226);
    #    """
    #)


def downgrade():
    op.execute(
        "UPDATE media SET parent_id = NULL WHERE name='Farm'"
    )

    op.execute(
        "UPDATE parameter_definition SET default_value = 0.0006 WHERE variable_name = 'AverageVerticalVelocity';"
    )

    #op.execute(
    #    """
    #    DELETE FROM parameter_definition WHERE variable_name = 'mixingHeight' AND domain_id = 1;
    #    """
    #)
