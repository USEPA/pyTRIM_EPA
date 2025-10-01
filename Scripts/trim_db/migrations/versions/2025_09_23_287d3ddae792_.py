"""
new EnrichmentRatio parameter for erosion that 
modifies the total erosion value based on the type of chemical (organic/non-organic)

Revision ID: 287d3ddae792
Revises: 0b7c18f6db0f
Create Date: 2025-09-23 11:09:58.947268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '287d3ddae792'
down_revision = '0b7c18f6db0f'
branch_labels = None
depends_on = None


target_pattern = 'sender.TotalErosionRate'
new_param = 'EnrichmentRatio'
new_param_eq = '3 if self.isa("Organic") else 1'
updated_val = f'chemical.{new_param} * {target_pattern}'
update_query = sa.text(
    f"UPDATE formula SET equation = :equation WHERE id = :id;"
)


def upgrade():
    conn = op.get_bind()

    curr = conn.execute(sa.text(
        f"INSERT INTO formula (equation) VALUES ('{new_param_eq}');"
    ))
    new_formula_id = curr.lastrowid

    conn.execute(sa.text(
        f"INSERT INTO parameter_definition (variable_name, full_name, domain_id, default_formula_id)"
        f" VALUES ('{new_param}', '{new_param}', 2, {new_formula_id});"
    ))

    select_query = sa.text(
        f"SELECT * FROM formula WHERE equation LIKE '%{target_pattern}%';"
    )
    for formula_row in conn.execute(select_query):
        eq = formula_row.equation
        new_eq = updated_val.join(eq.split(target_pattern))
        conn.execute(update_query, {'equation': new_eq, 'id': formula_row.id})


def downgrade():
    conn = op.get_bind()
    select_query = sa.text(
        f"SELECT * FROM formula WHERE equation LIKE '%{updated_val}%';"
    )
    for formula_row in conn.execute(select_query):
        eq = formula_row.equation
        old_eq = target_pattern.join(eq.split(updated_val))
        conn.execute(update_query, {'equation': old_eq, 'id': formula_row.id})

    conn.execute(sa.text(
        f"DELETE FROM parameter_definition WHERE variable_name = '{new_param}' AND domain_id = 2;"
    ))

    conn.execute(sa.text(
        f"DELETE FROM formula WHERE equation = '{new_param_eq}';"
    ))
