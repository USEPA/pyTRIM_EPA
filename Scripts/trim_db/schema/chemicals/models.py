import sqlalchemy as sa
from ..parameters.utils import use_linked_parameters
from ..utils.base import Model


__all__ = [
    'Chemical'
]


scenario_chemicals = sa.Table(
    'scenario_chemicals',
    Model.metadata,
    sa.Column(
        'scenario_id', sa.Integer(),
        sa.ForeignKey('scenario.id')
    ),
    sa.Column(
        'chemical_id', sa.Integer(),
        sa.ForeignKey('chemical.id')
    ),
    sa.UniqueConstraint('scenario_id', 'chemical_id'),
)


@use_linked_parameters
class Chemical(Model):
    name = sa.Column(sa.String(120), nullable=False)
    cas_number = sa.Column(sa.String(120), nullable=False)

    category = sa.Column(sa.String(240), nullable=False)

    _scenarios = sa.orm.relationship(
        'Scenario', secondary=scenario_chemicals,
        enable_typechecks=False,
        backref=sa.orm.backref(
            'chemicals', enable_typechecks=False
        )
    )

    # Each parcel should have a unique name in its scenario
    __table_args__ = (
        sa.UniqueConstraint('name', 'cas_number'),
    )

    def as_serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'cas_number': self.cas_number,
            'category': self.category
        }

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'{self.id}, "{self.name}", "{self.cas_number}"'
            ')'
        )
