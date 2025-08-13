"""
parameter definition value updates
interface_with adjustment

Revision ID: 151911e8b6a9
Revises: 12f3b3bc93f9
Create Date: 2025-08-12 08:34:21.909681

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "151911e8b6a9"
down_revision = "12f3b3bc93f9"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "UPDATE parameter_definition SET default_value = 100 WHERE variable_name='ReceptorSpacing'"
    )

    # must update .interface_with references within code as well
    op.execute(
        """
        UPDATE formula
        SET equation = REPLACE(equation, 'sender.volume_element.interface_with(receiver.volume_element)', 'sender.interface_with(receiver)')
        WHERE equation LIKE ('%sender.volume_element.interface_with(receiver.volume_element)%');
        """
    )

    # updates self.media_id == {media.id} to self.media.isa({media.name})
    # this is to include subdomains e.g. the surface soil domain is retrieved when working with tilled soil
    # must update trim_db/porting/scenarios.py and init_tillage_default_params as well
    conn = op.get_bind()
    for param_domain in conn.execute(sa.text("SELECT * FROM parameter_domain WHERE requirements IS NOT NULL")):
        media_id = param_domain.requirements.split(" == ")[1]
        media = conn.execute(
            sa.text(f'SELECT * FROM media WHERE id = :media_id'),
            ({'media_id': int(media_id)}),
        ).first()

        new_req = f'self.media.isa("{media.name}")'
        conn.execute(
            sa.text("UPDATE parameter_domain SET requirements = :requirement WHERE id = :id"),
            ({'requirement': new_req, 'id': param_domain.id}),
        )


def downgrade():
    op.execute(
        "UPDATE parameter_definition SET default_value = 0 WHERE variable_name='ReceptorSpacing'"
    )

    op.execute(
        """
        UPDATE formula
        SET equation = REPLACE(equation, 'sender.interface_with(receiver)', 'sender.volume_element.interface_with(receiver.volume_element)')
        WHERE equation LIKE ('%sender.interface_with(receiver)%');
        """
    )

    conn = op.get_bind()
    for param_domain in conn.execute(sa.text("SELECT * FROM parameter_domain WHERE requirements IS NOT NULL")):
        media_name = param_domain.requirements.replace('self.media.isa("', "").replace('")', "")
        media = conn.execute(
            sa.text(f'SELECT * FROM media WHERE name = :media_name'),
            ({'media_name': media_name}),
        ).first()

        new_req = f'self.media_id == {media.id}'
        conn.execute(
            sa.text("UPDATE parameter_domain SET requirements = :requirement WHERE id = :id"),
            ({'requirement': new_req, 'id': param_domain.id}),
        )
