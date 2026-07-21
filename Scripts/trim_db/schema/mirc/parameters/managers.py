from sqlalchemy import or_
from .models import MircParameter, ureg
from ...utils.serialize import register_serializer


__all__ = [
    'ParameterManager'
]


class NullParameter:
    def __init__(self, unit=''):
        self._value = 0
        self._unit = unit
        self._source = None

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit

    @property
    def quantity(self):
        return self._value * ureg(self._unit)

    @property
    def source(self):
        return self._source

    def __bool__(self):
        return False

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration

    def __getattr__(self, name):
        if name in dir(MircParameter):
            if isinstance(getattr(MircParameter, name), type(list.append)):
                return (lambda: None)
            return None
        else:
            raise AttributeError


@register_serializer(NullParameter)
def _ts_null_param(n: NullParameter):
    return None


class ParameterManager:
    """Mediates access to all variable parameters in a scenario.
    """

    _query_terms = {}

    def __init__(self, scenario, query_terms=None):
        self.scenario = scenario
        self._query_terms = {
            **(query_terms or {})
        }

    def __getattr__(self, name):
        return self.get_by_variable(name)

    def get_by_variable(self, variable):
        return self._get_param(variable=variable)

    def get_by_name(self, name):
        return self._get_param(name=name)

    def _get_param(self, **kwargs):
        s = self.scenario
        params = {}
        while s is not None:
            n_params = MircParameter.query.filter_by(
                scenario_id=s.id,
                **kwargs,
                **{
                    k + '_id': v.id
                    for k, v in self._query_terms.items()
                }
            ).all()
            n_keys = []
            for p in n_params:
                n_keys.append(
                    f'{p.chemical_id},{p.media_id},'
                    f'{p.life_stage_id},{p.percentile_id}'
                    f'{p.food_id},{p.name}'
                )
            n_params = dict(zip(n_keys, n_params))
            params = {**n_params, **params}
            s = s.parent

        if not params:
            return NullParameter(
                unit=self._get_param_default_dimensionality(**kwargs)
            )

        params = list(params.values())
        for param in params:
            if param.scenario.id != self.scenario.id:
                param.inherited = True
        if len(params) == 1:
            return params[0]
        else:
            return params

    def _get_param_default_dimensionality(self, name=None, variable=None):
        matching_params = MircParameter.query.filter(or_(
            MircParameter.name == name,
            MircParameter.variable == variable
        )).all()
        if not matching_params:
            return ''  # don't know
        matched_unit = matching_params[0].unit
        if matched_unit is None:
            return ''  # No unit
        return str(ureg.get_base_units(matched_unit)[-1])  # convert to base units

    def __iter__(self):
        return iter(self._get_param())  # List of all possible parameters

    def for_chemical(self, chemical):
        if isinstance(chemical, str):
            from ...entities.models import Chemical
            chemical = Chemical.query.filter_by(
                name=chemical
            ).first()
        elif isinstance(chemical, int):
            from ...entities.models import Chemical
            chemical = Chemical.query.get(chemical)

        if chemical is None:
            return self
        q = {
            **self._query_terms,
            'chemical': chemical
        }
        return ParameterManager(self.scenario, q)

    @property
    def chemical(self):
        return self._query_terms.get('chemical')

    def for_media(self, media):
        if isinstance(media, str):
            from ..builtins.models import MircProduct
            media = MircProduct.query.filter_by(name=media).first()
        elif isinstance(media, int):
            from ..builtins.models import MircProduct
            media = MircProduct.query.get(media)

        if media is None:
            return self
        q = {
            **self._query_terms,
            'media': media
        }
        return ParameterManager(self.scenario, q)

    @property
    def media(self):
        return self._query_terms.get('media')

    def at_life_stage(self, life_stage):
        if isinstance(life_stage, str):
            from ..builtins.models import MircLifeStage
            life_stage = MircLifeStage.query.filter_by(
                name=life_stage
            ).first()
        elif isinstance(life_stage, int):
            from ..builtins.models import MircLifeStage
            life_stage = MircLifeStage.query.get(life_stage)

        if life_stage is None:
            return self
        q = {
            **self._query_terms,
            'life_stage': life_stage
        }
        return ParameterManager(self.scenario, q)

    @property
    def life_stage(self):
        return self._query_terms.get('life_stage')

    def at_percentile(self, percentile):
        if isinstance(percentile, str):
            from ..builtins.models import MircPercentile
            percentile = MircPercentile.query.filter_by(
                name=percentile
            ).first()
        elif isinstance(percentile, int):
            from ..builtins.models import MircPercentile
            percentile = MircPercentile.query.get(percentile)

        if percentile is None:
            return self
        q = {
            **self._query_terms,
            'percentile': percentile
        }
        return ParameterManager(self.scenario, q)

    @property
    def percentile(self):
        return self._query_terms.get('percentile')

    def for_food(self, food):
        if isinstance(food, str):
            from ..builtins.models import MircProduct
            food = MircProduct.query.filter_by(name=food).first()
        elif isinstance(food, int):
            from ..builtins.models import MircProduct
            food = MircProduct.query.get(food)

        if food is None:
            return self
        q = {
            **self._query_terms,
            'food': food
        }
        return ParameterManager(self.scenario, q)

    @property
    def food(self):
        return self._query_terms.get('food')

    @property
    def unit_registry(self):
        return ureg

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}("
            f"{self.scenario.name}"
            f"{(', ' + self.chemical.cas_number) if self.chemical else ''}"
            f"{(', ' + self.media.name) if self.media else ''}"
            f"{(', ' + self.life_stage.name) if self.life_stage else ''}"
            f"{(', ' + self.percentile.name) if self.percentile else ''}"
            f"{(', ' + self.food.name) if self.food else ''}"
            ")"
        )


@register_serializer(ParameterManager)
def _ts_manager(pm: ParameterManager):
    return None
