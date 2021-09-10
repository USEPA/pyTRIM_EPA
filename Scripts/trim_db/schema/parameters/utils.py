import numpy as np
import sqlalchemy as sa
from pint import UnitRegistry
from simpleeval import simple_eval
from sqlalchemy.ext.declarative import declared_attr
from ..utils.base import Model


__all__ = [
    'use_linked_parameters'
]


ureg = UnitRegistry()


def as_quantity(val, unit=''):
    try:
        if val is None or not str(val) or np.isnan(val):
            return None
        if not unit:
            return val
        quantity = val * ureg(unit)

        if quantity.units == ureg.Unit(''):
            return val
        return quantity
    except TypeError:
        return None


def use_linked_parameters(cls):
    tbl = cls.__tablename__
    cls_nm = cls.__name__

    if cls_nm != 'Scenario':
        class ParameterMixin:
            @declared_attr
            def scenario_id(cls):
                return sa.Column(
                    sa.Integer(), sa.ForeignKey(f'scenario.id'),
                    nullable=False
                )
    else:
        class ParameterMixin:
            pass

    class Parameter(ParameterMixin, Model):
        __tablename__ = f'{tbl}_parameters'

        model_id = sa.Column(
            f'{tbl}_id', sa.Integer(), sa.ForeignKey(f'{tbl}.id'),
            nullable=False
        )

        scenario = sa.orm.relationship('Scenario', viewonly=True)

        name = sa.Column(sa.String(120), nullable=False)
        variable = sa.Column(sa.String(36), nullable=True)

        unique = sa.Column(sa.Boolean(), nullable=False, default=True)

        _val = sa.Column(sa.JSON(), nullable=False)

        @property
        def value(self):
            return (self._val or {}).get('value')

        @value.setter
        def value(self, v):
            if not self._val:
                self._val = {}
            if v is not None:
                try:
                    float(v)
                except (ValueError):
                    raise TypeError(
                        f'Invalid value type: {type(v)} ({v})'
                    ) from None
            self._val['value'] = v

        @property
        def unit(self):
            return (self._val or {}).get('unit')

        @unit.setter
        def unit(self, u):
            if not self._val:
                self._val = {}
            if u is not None:
                if not isinstance(u, str):
                    raise TypeError(
                        f'Invalid unit type: {type(u)} ({u})'
                    ) from None
            self._val['unit'] = u

        @property
        def quantity(self):
            return as_quantity(self.value, self.unit)

        @property
        def equation(self):
            alg = (self._val or {}).get('equation')
            if not alg:
                return None

            if not hasattr(self, '_func'):
                equation = deconstruct_equation(str(alg))

                var_map = {}
                for el in equation:
                    varname = el.split('.', 1)[-1]
                    if el.startswith('self.'):
                        param = self.model.parameters(
                            self.scenario
                        ).by_name(varname)
                    elif el.startswith('environment.'):
                        param = self.scenario.parameters.by_name(
                            varname
                        )
                    else:
                        continue

                    try:
                        if param.quantity:
                            param = param.quantity
                        elif param.equation:
                            param = param.equation(self.scenario)
                        else:
                            param = None
                    except AttributeError:
                        param = None
                    var_map[el] = param

                equation = ' '.join(equation)

                for el in list(var_map):
                    if '.' not in el:
                        continue
                    new_el = el.replace('.', '___')
                    equation = equation.replace(el, new_el)
                    var_map[new_el] = var_map[el]

                var_map = {k: v for k, v in var_map.items() if '.' not in k}
                var_map.update({'True': True, 'False': False})

                def func(scenario):
                    try:
                        ans = simple_eval(equation, names=var_map)
                    except TypeError:
                        # Replace longest keys first to avoid substring issues
                        eq = equation
                        keys = sorted(list(var_map), key=lambda x: len(x))
                        for k in reversed(keys):
                            v = var_map[k]
                            eq = eq.replace(str(k), str(v))
                        raise TypeError(
                            f'Invalid equation! "{eq}"'
                        )
                    return ans

                self._func = func

            return self._func

        @equation.setter
        def equation(self, eq):
            if not self._val:
                self._val = {}
            if eq is not None:
                eq = str(eq)
            self._val['equation'] = eq

        def __repr__(self):
            return (
                f'{cls_nm}Parameters('
                f'"{self.scenario.name}", "{self.name}", {self.quantity}'
                ')'
            )

    cls._parameters = sa.orm.relationship(
        Parameter,
        cascade='all, delete-orphan',
        backref=sa.orm.backref('model')
    )

    class ParameterManager:
        def __init__(self, model, scenario):
            self.model = model
            self.scenario = scenario

        def __getattr__(self, name):
            return self.by_name(name)

        @property
        def _parameters(self):
            if cls.__name__ == 'Scenario':
                k = 'model_id'
            else:
                k = 'scenario_id'
            if self.scenario is None:
                return list(sorted(
                    self.model._parameters, key=lambda x: getattr(x, k)
                ))
            return [
                x for x in self.model._parameters
                if getattr(x, k) == self.scenario.id
            ]

        def by_name(self, name):
            val = [
                x for x in self._parameters
                if x.name == name
            ]
            if not val:
                return None
            if val[0].unique:
                return val[0]
            return val

        def by_variable(self, variable):
            val = [
                x for x in self._parameters
                if x.variable == variable
            ]
            if not val:
                return None
            if val[0].unique:
                return val[0]
            return val

        def add(
            self, name, value=None, unit=None, equation=None,
            variable=None,
            unique=True
        ):
            if self.scenario is None:
                raise TypeError(
                    'Cannot add a parameter without specifying a scenario!'
                )
            param = Parameter(
                model=self.model,
                model_id=self.model.id,
                name=name, variable=variable, unique=unique
            )
            if cls.__name__ != 'Scenario':
                param.scenario_id = self.scenario.id
                param.scenario = self.scenario
            param.value = value
            param.unit = unit
            param.equation = equation

        def __repr__(self):
            if not self._parameters:
                return '[]'
            return (
                '[\n\t'
                + '\n\t'.join([str(x) for x in self._parameters])
                + '\n]'
            )

    if cls.__name__ == 'Scenario':
        cls.parameters = property(lambda x: ParameterManager(x, x))
    else:
        cls.parameters = lambda x, scenario=None: ParameterManager(x, scenario)

    return cls


def deconstruct_equation(equation):
    for char in '()+-*/=!':
        equation = equation.replace(char, f' {char} ')

    for double in ['**', '+=', '!=', '==']:
        d1 = double[0]
        d2 = double[1]
        equation.replace(f' {d1} {d2} ', f' {double} ')

    deconstructed = equation.split()
    return deconstructed
