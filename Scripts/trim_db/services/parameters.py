import numpy as np
from ..schema.scenarios.models import Scenario
from ..schema.parameters.models import *
from ..schema.parameters.utils import as_quantity
from ..schema.utils.caching import CacheManager
from .generic import GenericService

__all__ = ['FormulaService', 'ParameterService']


class FormulaService(GenericService):
    __model__ = Formula

    @classmethod
    def create(cls, *, no_commit=False, check_unique=True, **kwargs):
        model = super().create(
            no_commit=no_commit, check_unique=check_unique, **kwargs
        )
        with cls.db.session.no_autoflush:
            for arg in model.arguments.values():
                argname = arg.name.lower()
                classname = None

                if argname in ['environment', 'scenario']:
                    classname = 'Scenario'

                elif argname == 'chemical':
                    classname = 'Chemical'

                elif argname == 'volume_element':
                    classname = 'VolumeElement'

                elif argname in ['compartment', 'receiver', 'sender']:
                    classname = 'Compartment'

                elif argname == 'media':
                    classname = 'Media'

                if classname is not None:
                    arg.domain = ParameterService.domains.get_or_create(
                        name=classname, entity_type=classname, description=(
                            f'The default domain for {classname} Entities'
                        )
                    )
        if not no_commit and cls.auto_commit:
            cls.commit()
        return model


class ParameterService(GenericService):
    __model__ = CustomParameter

    class domains(GenericService):
        __model__ = ParameterDomain

    class definitions(GenericService):
        __model__ = ParameterDefinition


class NoneParameter(type(np.nan)):
    def __bool__(self):
        return False

    def __call__(self, *args, **kwargs):
        return np.nan

    @classmethod
    def instance(cls):
        try:
            obj = cls._instance
        except AttributeError:
            obj = super().__new__(cls)
            cls._instance = obj
        return obj

    def __init__(self):
        raise TypeError(
            f'{self.__class__.__qualname__} is a singleton,'
            ' and must be accessed using `instance()`.'
        )

    def __repr__(self):
        return 'NaN'


class classproperty:
    def __init__(self, f):
        self._f = f

    def __get__(self, obj, owner):
        return self._f(owner, obj)


def parameterize(cls):
    cls_name = cls.__name__

    def get_scenario(obj, scenario=None):
        if scenario is not None:
            CacheManager.clear_cache(f'entity_param::{cls_name}')
            setattr(obj, '__current_scenario', scenario)
        if getattr(obj, '__current_scenario', None) is None:
            from trim_db.services import ScenarioService
            s = ScenarioService.get_or_create(name='Default', creator_id=1)
            print(f"CACHE NOT CLEARED ... USING scenario {s.name}. cls name is {cls_name}")
            setattr(obj, '__current_scenario', s)
        return obj.__current_scenario

    if cls != Scenario:
        setattr(
            cls, 'current_scenario',
            lambda s, sc=None: get_scenario(s, sc)
        )

    def _get_current_scenario(entity):
        if entity == cls:
            raise AttributeError()  # Not defined
        elif isinstance(entity, Scenario):
            return entity
        elif not isinstance(entity, cls):
            raise NotImplementedError()
        else:
            return entity.current_scenario()

    # Make sure there is a default domain for this class
    def get_default_domain():
        default_domain = ParameterService.domains.get_or_create(
            name=cls_name, entity_type=cls_name,
            description=f'The default domain for {cls_name} Entities'
        )
        return default_domain

    # Define the function for getting the domains
    # of an entity with this class
    def get_domains(entity_cls, entity=None):
        if entity is None:
            entity = entity_cls
        possible_domains = ParameterService.domains.get_all(
            entity_type=cls_name
        )
        if not len(possible_domains):
            possible_domains.append(get_default_domain())

        if entity == cls:
            # Someone asked for Entity.domains;
            # give them everything possible for this class
            return possible_domains
        # Someone asked for Entity().domains;
        # give them everything possible for this _instance_ of the class
        domains = [d for d in possible_domains if d.validate(entity)]
        return domains

    setattr(cls, 'domains', classproperty(get_domains))

    # A class that allows you to get/set parameter definitions
    # (both globally for the class and custom for an instance of the class)
    class ParameterManager:
        def __init__(self, entity):
            self.entity = entity
            self._default_domain = get_default_domain()

        @property
        def _params(self):
            if self.entity == cls:
                # If called on the class
                # (e.g., Entity.parameters),
                # return all possible definitions
                return {
                    pd.name: pd
                    for d in self.entity.domains
                    for pd in d.parameter_definitions
                }
            else:
                # If called on an instance
                # (e.g., Entity().parameters),
                # return custom implementations of each definition,
                # or the definition itself
                # if no specific version applies
                p = {}
                for d in sorted(
                    # Sort to make sure sub-domains override parents
                    self.entity.domains,
                    key=lambda x: len(str(x.requirements or ''))
                ):
                    for pd in d.parameter_definitions:
                        if not len(pd.instances):
                            p[pd.name] = pd
                        else:
                            for cp in pd.instances:
                                if cp.validate(self.entity):
                                    p[pd.name] = cp
                                    break
                return p

        def __len__(self):
            return len(self._params)

        def __contains__(self, key):
            return key in self._params

        def __getitem__(self, key):
            return self._params[key]

        def get(self, key, default=None):
            return self._params.get(key, default)

        def __setitem__(self, key, value):
            raise NotImplementedError

        def add(
            self, name, domain=None,
            value=None, unit=None, formula=None,
            full_name=None, description=None,
            requirements=None, domain_name=None
        ):
            requirements = (requirements or '').strip()

            if domain is None:
                # Get the appropriate domain
                if domain_name is not None:
                    domain = ParameterService.domains.get(name=domain_name)
                if domain is None:
                    domain = self._default_domain

                if (
                    self.entity == cls
                    and requirements != (domain.requirements or '')
                ):
                    # If this was called on the class
                    # (e.g., Entity.parameters.add)
                    # but custom requirements were provided,
                    # this must be a parameter in a new sub-domain
                    # for this class
                    # Go ahead and get/create that subdomain
                    if domain_name is None:
                        domain_name = f'{cls_name} "{requirements}"'
                    domain = ParameterService.domains.get_or_create(
                        name=domain_name, entity_type=cls_name,
                        requirements=requirements
                    )

            pd_base = ParameterService.definitions.get(
                variable_name=name,
                full_name=full_name or name
            )

            pd = None
            if pd_base is not None:
                pd = pd_base
                if pd.domain.is_subdomain(domain):
                    pd.domain = domain
                elif not pd.domain.is_superdomain(domain):
                    pd = None
            if pd is None:
                pd = ParameterService.definitions.get_or_create(
                    variable_name=name,
                    full_name=full_name or name,
                    domain=domain
                )

            if description is not None:
                pd.description = description

            if self.entity == cls:
                # If this was called on the class
                # (e.g., Entity.parameters.add),
                # just update the parameter definition
                pd.default_value = value
                pd.default_unit = unit

                if isinstance(formula, str):
                    if (
                        pd.default_formula is None
                        or pd.default_formula.equation != formula
                    ):
                        pd.default_formula = FormulaService.create(
                            equation=formula
                        )
                        for arg in pd.default_formula.arguments.values():
                            if arg.name == 'self' and arg.domain is None:
                                arg.domain = domain

            else:
                # If this was called on an instance of the class
                # (e.g., Entity().parameters.add),
                # add a custom parameter for that instance
                if requirements:
                    requirements = f'({requirements}) and '
                requirements += f'(self.id == {self.entity.id})'

                current_scenario_id = _get_current_scenario(self.entity).id

                cp = ParameterService.get_or_create(
                    scenario_id=current_scenario_id,
                    definition_id=pd.id,
                    requirements=requirements,
                    no_commit=True
                )
                cp.value = value
                cp.unit = unit

                f = None
                if isinstance(formula, str):
                    if (
                        cp.formula is None
                        or cp.formula.equation != formula
                    ):
                        cp.formula = FormulaService.create(equation=formula)
                        f = cp.formula

                # Also update the defaults if none existed before,
                # to try and be helpful to the user if they make
                # more instances of this
                if unit and pd.default_unit is None:
                    pd.default_unit = unit
                if f is not None:
                    for arg in f.arguments.values():
                        if arg.name == 'self' and arg.domain is None:
                            arg.domain = domain

                    if pd.default_formula is None:
                        pd.default_formula = f

            ParameterService.commit()
            self._params[name] = pd

        def keys(self):
            return self._params.keys()

        def values(self):
            return self._params.values()

        def items(self):
            return self._params.items()

        def __repr__(self):
            return f'{{{", ".join([str(x) for x in self.keys()])}}}'

    def get_manager(entity_cls, entity=None):
        if entity is None:
            # Someone asked for Entity.parameters;
            # give them a manager for this entire class
            entity = entity_cls
        # Someone asked for Entity().parameters;
        # give them a manager for this _instance_ of the class
        return ParameterManager(entity)

    # Define the function for getting the parameters
    # of an entity with this class
    setattr(cls, 'parameters', classproperty(get_manager))

    def convert_unit(val, unit, strict=False):
        if not hasattr(val, 'dimensionality'):
            val = as_quantity(val, unit)
        else:
            if not strict and unit:
                val = val.magnitude
            try:
                val = as_quantity(val, unit)
            except Exception:
                print(val)
                print(unit)
                raise
        return val

    def partial_formula(
        formula, default_kwargs, unit, strict_units=False
    ):
        def wrapped(*args, **kwargs):
            opts = dict(default_kwargs)
            opts.update(kwargs)
            val = formula.eval(*args, **opts)
            val = convert_unit(val, unit, strict=strict_units)
            return val
        return wrapped

    # A method to get the VALUE of a parameter
    @CacheManager.with_caching(f'entity_param::{cls_name}')
    def get_parameter(
        entity, name, strict_units=False, default=NoneParameter.instance()
    ):
        if name.startswith('_') or name in ['parameters']:
            raise AttributeError()

        # This method of accessing parameters exists for legacy reasons,
        # so it only needs to work for code like "Entity().param_name".
        # Calling "Entity.param_name" is NOT supported
        param = entity.parameters.get(name, default)
        if (
            isinstance(param, ParameterDefinition)
            or isinstance(param, CustomParameter)
        ):
            if isinstance(param, CustomParameter):
                unit = param.unit or ''
            else:
                unit = param.default_unit or ''

            q = param.quantity
            if isinstance(q, Formula):
                arguments = {}
                if 'self.' in q.equation:
                    arguments['self'] = entity
                if 'environment.' in q.equation:
                    arguments['environment'] = _get_current_scenario(entity)
                try:
                    val = q.eval(**arguments)
                except TypeError as e:
                    if 'Missing argument' in str(e):
                        return partial_formula(
                            q, arguments, unit, strict_units=strict_units
                        )
                    raise
            else:
                val = q
            val = convert_unit(val, unit, strict=strict_units)
            return val
        return default

    # Override getattr
    setattr(cls, '__getattr__', get_parameter)

    return cls
