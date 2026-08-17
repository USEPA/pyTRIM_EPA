import sqlalchemy as sa
from ..parameters.models import as_quantity
from ..parameters.managers import ParameterManager
from ...utils.base import Model
from ...utils.mixins import TrackUpdatesMixin
from ...utils.permissions import require_permissions, PermissionsEnum
from ...utils.serialize import register_serializer


__all__ = [
    'MircScenario',
    'MircSimulation', 'MircSimulationPercentile',
    'MircSimulationParameter', 'MircSimulationConsumptionBreakdown'
]


@require_permissions(
    allow_keys={'creator_id': PermissionsEnum.manage},
    custom_allow=(lambda mirc_scenario, user: mirc_scenario.is_builtin)
)
class MircScenario(Model):
    """Represents an ingestion scenario, and provides access
    to all parameters for performing MIRC calculations.
    """
    name = sa.Column(sa.String(255), unique=False, nullable=False)
    is_builtin = sa.Column(sa.Boolean(), nullable=False, default=False)
    notes = sa.Column(sa.String(800))

    parent_id = sa.Column(
        sa.Integer(),
        sa.ForeignKey('mirc_scenario.id'),
        nullable=True
    )
    parent = sa.orm.relationship(
        'MircScenario', remote_side='MircScenario.id',
        backref=sa.orm.backref("child_scenarios")
    )

    @property
    def parameters(self):
        return ParameterManager(self)

    @property
    def priority_chemicals(self):
        # Hard-coding this for now, but putting it here
        # makes it possible to make this per-scenario later on
        # if we want
        from ...entities.chemicals import Chemical
        from ..builtins.models import PRIORITY_CHEMICALS
        priority = [
            c for c in Chemical.query.all()
            if c.cas_number in PRIORITY_CHEMICALS
        ]
        return priority

    def __repr__(self):
        return f"{self.__class__.__qualname__}('{self.name}')"


@register_serializer(MircScenario, queryable=True, auto_recursive=False)
def _ts_scenario(scenario: MircScenario):
    p = None
    if scenario.parent:
        p = {
            'id': scenario.parent.id,
            'name': scenario.parent.name
        }
    return {
        'id': scenario.id,
        'name': scenario.name,
        'parent': p,
        'notes': scenario.notes
    }


class MircSimulation(Model, TrackUpdatesMixin):
    name = sa.Column(sa.String(120), nullable=False)

    trim_scenario_id = sa.Column(
        sa.Integer(), sa.ForeignKey('scenario.id'), nullable=False
    )
    trim_scenario = sa.orm.relationship(
        'Scenario',
        backref=sa.orm.backref(
            'mirc_simulations', cascade="all, delete-orphan", single_parent=True
        )
    )

    mirc_scenario_id = sa.Column(
        sa.Integer(), sa.ForeignKey('mirc_scenario.id'), nullable=False
    )
    mirc_scenario = sa.orm.relationship(
        'MircScenario', backref=sa.orm.backref('simulations')
    )

    chemical_id = sa.Column(
        sa.Integer(), sa.ForeignKey('chemical.id'), nullable=False
    )
    chemical = sa.orm.relationship('Chemical')

    use_baf = sa.Column(sa.Boolean(), nullable=False, default=False)

    def get_parameter(self, variable=None, name=None):
        for p in self.parameters:
            if variable is not None and p.variable == variable:
                return p
            elif name is not None and p.name == name:
                return p
        return None

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}("
            f"'{self.trim_scenario.name}', '{self.name}'"
            ")"
        )


@register_serializer(MircSimulation, queryable=True)
def _ts_simulation(simulation: MircSimulation):
    return {
        'id': simulation.id,
        'name': simulation.name,
        'chemical': {
            'name': simulation.chemical.hap_name or simulation.chemical.name,
            'cas_number': simulation.chemical.cas_number
        }
    }


class MircSimulationPercentile(Model):
    simulation_id = sa.Column(
        sa.Integer(), sa.ForeignKey('mirc_simulation.id'), nullable=False
    )
    simulation = sa.orm.relationship(
        'MircSimulation',
        backref=sa.orm.backref(
            'percentiles', cascade="all, delete-orphan",
            single_parent=True,
            lazy='joined'
        )
    )

    food_id = sa.Column(
        sa.Integer(), sa.ForeignKey('mirc_product.id'), nullable=True
    )
    food = sa.orm.relationship('MircProduct')

    percentile_id = sa.Column(
        sa.Integer(), sa.ForeignKey('mirc_percentile.id'), nullable=False
    )
    percentile = sa.orm.relationship('MircPercentile')

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}("
            f"'{self.simulation.name}', "
            f"{(self.food.name + ', ') if self.food else 'body weight, '}"
            f"{self.percentile}"
            ")"
        )


class MircSimulationParameter(Model):
    simulation_id = sa.Column(
        sa.Integer(), sa.ForeignKey('mirc_simulation.id'), nullable=False
    )
    simulation = sa.orm.relationship(
        'MircSimulation',
        backref=sa.orm.backref(
            'parameters', cascade="all, delete-orphan",
            single_parent=True,
            lazy='joined'
        )
    )

    variable = sa.Column(sa.String(60), nullable=False)
    name = sa.Column(sa.String(255), nullable=True)

    value = sa.Column(sa.Float(), nullable=False)
    unit = sa.Column(sa.String(36), nullable=True)

    source = sa.Column(sa.String(255), nullable=True)

    @property
    def quantity(self):
        return as_quantity(self.value, self.unit)

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}("
            f"'{self.simulation.name}', {self.variable}, {self.quantity}, source='{self.source or ''}'"
            ")"
        )


@register_serializer(MircSimulationParameter)
def _ts_simulation_parameter(param: MircSimulationParameter):
    return {
        'id': param.id,
        'full_name': param.name or '',
        'variable_name': param.variable,
        'value': param.value,
        'unit': param.unit or '',
        'source': param.source or ''
    }


class MircSimulationConsumptionBreakdown(Model):
    simulation_id = sa.Column(
        sa.Integer(), sa.ForeignKey('mirc_simulation.id'), nullable=False
    )
    simulation = sa.orm.relationship(
        'MircSimulation',
        backref=sa.orm.backref(
            'consumption_breakdowns', cascade="all, delete-orphan",
            single_parent=True,
            lazy='joined'
        )
    )

    subfood_id = sa.Column(
        sa.Integer(), sa.ForeignKey('mirc_product.id'), nullable=False
    )
    subfood = sa.orm.relationship('MircProduct')

    fraction = sa.Column(sa.Float(), nullable=False)

    source = sa.Column(sa.String(255), nullable=True)

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}("
            f"'{self.simulation.name}', {self.subfood.name}, {self.fraction}"
            ")"
        )
