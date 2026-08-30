import numpy as np
import sqlalchemy as sa
from ...parameters.utils import ureg
from ...utils.base import Model
from ...utils.serialize import register_serializer


__all__ = [
    'MircParameter', 'MircToxicityEffect'
]


def as_quantity(val, unit=''):
    if val is None or not str(val) or np.isnan(val):
        return None
    if not unit:
        return val

    quantity = val * ureg(unit)

    if quantity.units == ureg.Unit(''):
        return val

    return quantity


# Declare table for mapping toxicity effects
parameter_toxicity = sa.Table(
    'mirc_parameter_toxicity',
    Model.metadata,
    sa.Column(
        'parameter_id', sa.Integer(),
        sa.ForeignKey('mirc_parameter.id')
    ),
    sa.Column(
        'toxicity_effect_id', sa.Integer(),
        sa.ForeignKey('mirc_toxicity_effect.id')
    )
)


class MircParameter(Model):
    scenario_id = sa.Column(
        sa.Integer(),
        sa.ForeignKey('mirc_scenario.id'),
        nullable=False
    )

    scenario = sa.orm.relationship(
        'MircScenario',
        backref=sa.orm.backref("_parameters", lazy='joined', cascade='all, delete-orphan')
    )

    name = sa.Column(sa.String(255), nullable=False)
    variable = sa.Column(sa.String(36), nullable=True)

    value = sa.Column(sa.Float(), nullable=False)
    unit = sa.Column(sa.String(36), nullable=True)

    source = sa.Column(sa.String(255))
    notes = sa.Column(sa.String(255))

    @property
    def quantity(self):
        return as_quantity(self.value, self.unit)

    inherited = False  # Dummy value; filled in by parameter managers

    chemical_id = sa.Column(
        sa.Integer(),
        sa.ForeignKey('chemical.id'),
        nullable=True
    )
    chemical = sa.orm.relationship(
        'Chemical',
        backref=sa.orm.backref(
            "_mirc_parameters", cascade="all, delete-orphan"
        )
    )

    media_id = sa.Column(
        sa.Integer(),
        sa.ForeignKey('mirc_product.id'),
        nullable=True
    )
    media = sa.orm.relationship(
        'MircProduct', foreign_keys=[media_id],
        backref=sa.orm.backref(
            "_parameters", cascade="all, delete-orphan"
        )
    )

    food_id = sa.Column(
        sa.Integer(),
        sa.ForeignKey('mirc_product.id'),
        nullable=True
    )
    food = sa.orm.relationship(
        'MircProduct', foreign_keys=[food_id]
    )

    life_stage_id = sa.Column(
        sa.Integer(),
        sa.ForeignKey('mirc_life_stage.id'),
        nullable=True
    )
    life_stage = sa.orm.relationship(
        'MircLifeStage',
        backref=sa.orm.backref(
            "_parameters", cascade="all, delete-orphan"
        )
    )

    percentile_id = sa.Column(
        sa.Integer(),
        sa.ForeignKey('mirc_percentile.id'),
        nullable=True
    )
    percentile = sa.orm.relationship(
        'MircPercentile',
        backref=sa.orm.backref(
            "_parameters", cascade="all, delete-orphan"
        )
    )

    toxicity_effects = sa.orm.relationship(
        'MircToxicityEffect', secondary=parameter_toxicity,
        enable_typechecks=False,
        backref=sa.orm.backref(
            'parameters', lazy='dynamic', enable_typechecks=False
        )
    )

    def __iter__(self):
        return iter([self])

    __table_args__ = (
        sa.UniqueConstraint(
            'scenario_id', 'chemical_id', 'media_id',
            'life_stage_id', 'percentile_id', 'food_id',
            'name'
        ),
    )

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}"
            f"('{self.scenario.name}', '{self.name}', "
            f"{(self.chemical.cas_number + ', ') if self.chemical else ''}"
            f"{(self.media.name + ', ') if self.media else ''}"
            f"{(self.life_stage.name + ', ') if self.life_stage else ''}"
            f"{(self.percentile.name + ', ') if self.percentile else ''}"
            f"{self.quantity}"
            f"{(' ' + self.food.name) if self.food else ''}"
            ")"
        )


@register_serializer(MircParameter)
def _ts_param(param: MircParameter):
    s = {
        'scenario': param.scenario.name,
        'media': param.media.name if param.media else None,
        'chemical': {
            'cas_number': param.chemical.cas_number,
            'hap_name': param.chemical.hap_name,
            'name': param.chemical.name
        } if param.chemical else None,
        'life_stage': param.life_stage.name if param.life_stage else None,
        'percentile': param.percentile.name if param.percentile else None,
        'food': param.food.name if param.food else None,
        'name': param.name,
        'variable': param.variable,
        'value': param.value,
        'unit': param.unit,
        'toxicity_effects': (
            param.toxicity_effects if param.toxicity_effects else None
        ),
        'source': param.source if param.metadata else None,
        'notes': param.notes if param.metadata else None,
        'inherited': param.inherited
    }
    return {k: v for k, v in s.items() if v is not None}


class MircToxicityEffect(Model):
    description = sa.Column(sa.String(255), unique=True)

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}"
            f"('{self.description}')"
        )
