"""
Farm media
AverageVerticalVelocity
Aquatic food web

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

    # Aquatic food web default values   
    op.execute( # Benthic_Carnivore
        """
        INSERT INTO parameter_definition (variable_name, full_name, domain_id, default_value, default_unit) 
        VALUES ('BiomassPerArea', 'BiomassPerArea', 9, 0.001, 'kg/m^2');
        """
    )
    op.execute( # Benthic_Omnivore
        """
        INSERT INTO parameter_definition (variable_name, full_name, domain_id, default_value, default_unit) 
        VALUES ('BiomassPerArea', 'BiomassPerArea', 11, 0.002, 'kg/m^2');
        """
    )
    op.execute( # Water_Column_Carnivore
        """
        INSERT INTO parameter_definition (variable_name, full_name, domain_id, default_value, default_unit) 
        VALUES ('BiomassPerArea', 'BiomassPerArea', 34, 0.0002, 'kg/m^2');
        """
    )
    op.execute( # Water_Column_Herbivore
        """
        INSERT INTO parameter_definition (variable_name, full_name, domain_id, default_value, default_unit) 
        VALUES ('BiomassPerArea', 'BiomassPerArea', 35, 0.002, 'kg/m^2');
        """
    )
    op.execute( # Water_Column_Omnivore
        """
        INSERT INTO parameter_definition (variable_name, full_name, domain_id, default_value, default_unit) 
        VALUES ('BiomassPerArea', 'BiomassPerArea', 36, 0.0005, 'kg/m^2');
        """
    )
    op.execute( # Zooplankton
        """
        INSERT INTO parameter_definition (variable_name, full_name, domain_id, default_value, default_unit) 
        VALUES ('BiomassPerArea', 'BiomassPerArea', 37, 0.0064, 'kg/m^2');
        """
    )

    op.execute( # Macrophyte
        "UPDATE parameter_definition SET default_value = 0.5 WHERE domain_id = 23 AND variable_name = 'BiomassPerArea';"
    )
    op.execute( # Benthic_Omnivore
        "UPDATE parameter_definition SET default_value = 0.25 WHERE domain_id = 11 AND variable_name = 'BW';"
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

    op.execute(
        """
            DELETE FROM parameter_definition WHERE variable_name = 'BiomassPerArea' 
            AND domain_id IN (9, 11, 34, 35, 36, 37);
        """
    )
    op.execute( # Macrophyte
        "UPDATE parameter_definition SET default_value = 0.6 WHERE domain_id = 23 AND variable_name = 'BiomassPerArea';"
    )
    op.execute( # Benthic_Omnivore
        "UPDATE parameter_definition SET default_value = 2 WHERE domain_id = 11 AND variable_name = 'BW';"
    )
