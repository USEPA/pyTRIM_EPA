import sqlalchemy as sa
from ..utils.base import Model
from ..utils.caching import CacheManager
from ..utils.serialize import register_serializer
from .equations import *
from .utils import *

__all__ = [
    'ParameterDomain', 'ParameterDefinition', 'CustomParameter',
    'Formula', 'FormulaArgument',
    'ureg'
]


class ParameterDomain(Model):
    name = sa.Column(sa.String(120), nullable=False)
    entity_type = sa.Column(sa.String(120), nullable=False)
    requirements = sa.Column(sa.String())

    description = sa.Column(sa.String(240))

    __table_args__ = (
        sa.UniqueConstraint('entity_type', 'requirements'),
    )

    def validate(self, entity):
        if not entity.__class__.__name__ == self.entity_type:
            return False

        if not (self.requirements or '').strip():
            return True

        if not hasattr(self, '_validator'):
            setattr(self, '_validator', as_function(self.requirements))
        return self._validator(self=entity) or False

    def is_subdomain(self, domain):
        if self.entity_type != domain.entity_type:
            return False
        if (domain.requirements or '') not in (self.requirements or ''):
            return False
        return True

    def is_superdomain(self, domain):
        return domain.is_subdomain(self)

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            + f'"{self.name}"'
            + (f', "{self.entity_type}"' if self.entity_type != self.name else '')  # noqa
            + (f', "{self.requirements}"' if self.requirements else '')
            + ')'
        )


class Formula(Model):
    _equation = sa.Column('equation', sa.String(), nullable=False)

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Formula.equation must be of type str')
        try:
            delattr(self, '_compiled')
        except AttributeError:
            pass  # It wasn't there anyway
        try:
            delattr(self, '_args')
        except AttributeError:
            pass  # It wasn't there anyway
        eq = deconstruct_equation(str(value))

        val = (' '.join(eq) if ' ' in str(value) else ''.join(eq))
        for brackets in ['..', '()', '[]', '{}']:
            val = val.replace(f'{brackets[0]} ', brackets[0])
            val = val.replace(f' {brackets[1]}', brackets[1])

        self._equation = val
        self.arguments  # access this to load args

    description = sa.Column(sa.String(240))

    # Use `self_` instead of `self` here because we want the caller
    # to be able to pass _itself_ as `self` to the equation
    # (if it needs to)
    def evaluate(
        self_, *args, IGNORE_EXTRA=False, **kwargs
    ):
        @CacheManager.with_caching(f'formula::{self_.id}')
        def cached_eval(IGNORE_EXTRA, *args, **kwargs):
            positional_args = list(args)
            combined_args = dict(kwargs)
            # print(f'eval({self_})')

            if not IGNORE_EXTRA:
                for k, v in combined_args.items():
                    if k == 'self':
                        continue
                    if k not in self_.arguments.keys():
                        raise TypeError(
                            f'"{self_.equation}" got an unexpected argument'
                            f' "{k}"'
                        )
                    arg = self_.arguments.get(k)
                    if arg is not None:
                        if not arg.validate(v):
                            raise TypeError(
                                f'[{v}] is not a valid value '
                                f'for argument "{k}" in "{self_.equation}"'
                            )

            for k, arg_def in self_.arguments.items():
                if k in combined_args:
                    continue
                if positional_args:
                    for x in positional_args:
                        if arg_def.validate(x):
                            combined_args[k] = x
                            positional_args.remove(x)
                        break
                    if k in combined_args:
                        continue
                raise TypeError(
                    f'Missing argument "{k}" for "{self_.equation}"'
                )

            if not hasattr(self_, '_compiled'):
                setattr(self_, '_compiled', as_function(self_.equation))
            return self_._compiled(**combined_args)

        return cached_eval(IGNORE_EXTRA, *args, **kwargs)

    # Use `self_` instead of `self` here because we want the caller
    # to be able to pass _itself_ as `self` to the equation
    # (if it needs to)
    def eval(self_, *args, **kwargs):
        try:
            return self_.evaluate(*args, **kwargs)
        except IndexError:
            print(self_)
            print(args)
            print(kwargs)
            raise

    @property
    def arguments(self):
        if not hasattr(self, '_args'):
            setattr(self, '_args', ArgumentManager(self))
        return self._args

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            + f'{self.equation}'
            + ')'
        )


class ArgumentManager:
    def __init__(self, formula):
        self.__formula = formula

        old_args = {x.name: x for x in formula._arguments}
        new_args = [x.split('.')[0] for x in find_arguments(formula.equation)]

        for x in list(old_args):
            if x not in new_args:
                formula._arguments = []
                old_args = {}
                break

        for x in set(new_args):
            if not x:
                continue
            if x not in old_args:
                formula._arguments.append(FormulaArgument(name=x))

        self.__args = {x.name: x for x in formula._arguments}

    def __len__(self):
        return len(self.__args)

    def __contains__(self, key):
        return key in self.__args

    def __getitem__(self, key):
        return self.__args[key]

    def get(self, key, default=None):
        return self.__args.get(key, default)

    def __setitem__(self, key, value):
        if not isinstance(value, FormulaArgument):
            raise TypeError(f'Invalid argument type: {type(value)}')
        if '.' in key:
            raise ValueError(f'Argument names cannot contain the symbol .')
        value.formula = self.__formula
        self.__args[key] = value

    def add(self, value):
        if not isinstance(value, FormulaArgument):
            raise TypeError(f'Invalid argument type: {type(value)}')
        if '.' in value.name:
            raise ValueError(f'Argument names cannot contain the symbol .')
        value.formula = self.__formula
        self.__args[value.name] = value

    def keys(self):
        return self.__args.keys()

    def values(self):
        return self.__args.values()

    def items(self):
        return self.__args.items()

    def __repr__(self):
        return (
            '{'
            + ','.join(f"'{k}': {v}" for k, v in self.items())
            + '}'
        )


class FormulaArgument(Model):
    formula_id = sa.Column(
        sa.Integer(), sa.ForeignKey('formula.id'), nullable=False
    )
    formula = sa.orm.relationship(
        'Formula', backref=sa.orm.backref('_arguments')
    )

    name = sa.Column(sa.String(60), nullable=False)

    domain_id = sa.Column(
        sa.Integer(), sa.ForeignKey('parameter_domain.id'), nullable=True
    )
    domain = sa.orm.relationship('ParameterDomain')

    def validate(self, arg):
        if self.domain is None:
            return True
        return self.domain.validate(arg)

    # Each argument should have a unique name in its formula
    __table_args__ = (
        sa.UniqueConstraint('formula_id', 'name'),
    )

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            + f'formula_id={self.formula.id}, "{self.name}"'
            + ')'
        )


class ParameterDefinition(Model):
    variable_name = sa.Column(sa.String(60), nullable=False)
    full_name = sa.Column(sa.String(120), nullable=False)

    @property
    def name(self):
        return self.variable_name

    @name.setter
    def name(self, value):
        self.variable_name = value

    description = sa.Column(sa.String(240))

    domain_id = sa.Column(
        sa.Integer(), sa.ForeignKey('parameter_domain.id'), nullable=False
    )
    domain = sa.orm.relationship(
        'ParameterDomain',
        backref=sa.orm.backref('parameter_definitions')
    )

    default_value = sa.Column(sa.Float())
    default_unit = sa.Column(sa.String(60))

    default_formula_id = sa.Column(
        sa.Integer(), sa.ForeignKey('formula.id')
    )
    default_formula = sa.orm.relationship('Formula')  # , lazy='subquery' ASK JOSIAH

    @property
    def value(self):
        return self.default_value

    @property
    def unit(self):
        return self.default_unit

    @property
    def formula(self):
        return self.default_formula

    @property
    def quantity(self):
        return self.default_quantity

    @property
    def default_quantity(self):
        if self.default_value is not None:
            return as_quantity(self.default_value, self.default_unit)
        elif self.default_formula is not None:
            return self.default_formula
        return None

    def evaluate(self, entity):
        if not self.domain.validate(entity):
            raise TypeError(
                f'"{self.name}" is not defined'
                f' for {type(entity)} entities'
            )
        for customized in self.instances:
            if customized.validate(entity):
                return customized.quantity
        return self.default_quantity

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            + f'"{self.domain.name}", "{self.name}", {self.default_quantity}'
            + ')'
        )


@register_serializer(ParameterDefinition)
def serialize_parameter_definition(pd: ParameterDefinition):
    s = {
        'name': pd.variable_name,
        'value': pd.default_value,
        'unit': pd.default_unit,
        'formula': pd.default_formula.equation if pd.default_formula else None
    }
    return s


class CustomParameter(Model):
    definition_id = sa.Column(
        sa.Integer(), sa.ForeignKey('parameter_definition.id'), nullable=False
    )
    definition = sa.orm.relationship(
        'ParameterDefinition',
        backref=sa.orm.backref('instances')
    )

    scenario_id = sa.Column(
        sa.Integer(), sa.ForeignKey('scenario.id'), nullable=False
    )
    # scenario = sa.orm.relationship('Scenario')

    scenario = sa.orm.relationship(
        'Scenario', backref=sa.orm.backref('custom_params', lazy='dynamic')
    )

    @property
    def domain(self):
        return self.definition.domain

    @property
    def domain_id(self):
        return self.definition.domain_id

    @property
    def variable_name(self):
        return self.definition.variable_name

    requirements = sa.Column(sa.String())

    def validate(self, entity):
        if not self.definition.domain.validate(entity):
            return False

        if not (self.requirements or '').strip():
            return True

        if not hasattr(self, '_validator'):
            setattr(self, '_validator', as_function(self.requirements))
        return self._validator(self=entity) or False

    value = sa.Column(sa.Float())
    unit = sa.Column(sa.String(60))

    formula_id = sa.Column(
        sa.Integer(), sa.ForeignKey('formula.id')
    )
    formula = sa.orm.relationship('Formula')  # , lazy='subquery' ASK JOSIAH

    @property
    def quantity(self):
        if self.value is not None:
            u = self.unit or self.definition.default_unit
            return as_quantity(self.value, u)
        elif self.formula is not None:
            return self.formula

    @property
    def default_quantity(self):
        return self.definition.default_quantity

    def evaluate(self, entity):
        if not self.validate(entity):
            raise TypeError(
                f'"{self.definition.name}" is not customized'
                f' for {type(entity)} entities'
            )
        return self.quantity

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            + f'{self.scenario}, "{self.definition.domain.name}",'
            + f' "{self.definition.name}", {self.quantity}'
            + ')'
        )


@register_serializer(CustomParameter)
def serialize_custom_parameter(cp: CustomParameter):
    s = {
        'name': cp.variable_name,
        'value': cp.value,
        'unit': cp.unit,
        'formula': cp.formula.equation if cp.formula else None
    }
    return s