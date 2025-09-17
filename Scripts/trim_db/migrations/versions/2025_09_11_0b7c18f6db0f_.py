"""
Model run updates
Meteorology default values
Seasonal dynamics default values

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
    #op.execute(
    #    "ALTER TABLE scenario_load_run_proc ADD COLUMN execution_arn VARCHAR(255);"
    #)

    op.execute("UPDATE parameter_definition SET default_value = 0.5 WHERE variable_name = 'isDay_Dynamic';")

    op.execute("UPDATE parameter_definition SET default_value = 1 WHERE variable_name = 'AllowExchange_forAir';")

    # TODO check sd domains
    # fixing incorrect litterfall domains -- no particle
    op.execute("UPDATE parameter_definition SET domain_id = 16 WHERE variable_name = 'LitterFallRate' AND domain_id = 20;") # coniferous
    op.execute("UPDATE parameter_definition SET domain_id = 15 WHERE variable_name = 'LitterFallRate' AND domain_id = 19;") # agriculture
    op.execute("UPDATE parameter_definition SET domain_id = 17 WHERE variable_name = 'LitterFallRate' AND domain_id = 21;") # deciduous
    op.execute("UPDATE parameter_definition SET domain_id = 18 WHERE variable_name = 'LitterFallRate' AND domain_id = 22;") # grass

    # coniferous (domain 20) = 0.0021, all others = 0.0126
    op.execute("UPDATE parameter_definition SET default_value = 0.0126 WHERE variable_name = 'LitterFallRate';")
    op.execute("UPDATE parameter_definition SET default_value = 0.0021 WHERE variable_name = 'LitterFallRate' AND domain_id = 16;")


def downgrade():
    #op.execute(
    #    "ALTER TABLE scenario_load_run_proc DROP COLUMN execution_arn;"
    #)

    op.execute("UPDATE parameter_definition SET default_value = 1 WHERE variable_name = 'isDay_Dynamic';"
    )

    op.execute("UPDATE parameter_definition SET default_value = NULL WHERE variable_name = 'AllowExchange_forAir';")
    op.execute("UPDATE parameter_definition SET default_value = 0.0021 WHERE variable_name = 'AllowExchange_forAir' AND domain_id = 3;")