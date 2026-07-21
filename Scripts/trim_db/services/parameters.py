from sqlalchemy import or_
from ..schema.scenarios.models import Scenario
from ..schema.parameters.models import *
from ..schema.parameters.utils import as_quantity, NoneParameter
from ..schema.utils.caching import CacheManager
from .generic import GenericService
from .utils import *

__all__ = ['FormulaService', 'ParameterService']


class FormulaService(GenericService[Formula]):
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


class ParameterService(GenericService[CustomParameter]):
    __model__ = CustomParameter

    class domains(GenericService[ParameterDomain]):
        __model__ = ParameterDomain

    class definitions(GenericService[ParameterDefinition]):
        __model__ = ParameterDefinition

        @classmethod
        def get_all_for_domain(cls, domain):
            if isinstance(domain, int):
                return cls.get_all(domain_id=domain)
            elif isinstance(domain, ParameterDomain):
                return cls.get_all(domain_id=domain.id)
            elif isinstance(domain, str):
                domain = ParameterService.domains.get(name=domain)
                return cls.get_all(domain_id=domain.id)

    @classmethod
    def get_custom_parameters_by_name(cls, name, scenario_id=None):
        query = cls.db.session.query(CustomParameter).join(
            ParameterDefinition, ParameterDefinition.id == CustomParameter.definition_id
        ).filter(
            ParameterDefinition.variable_name == name
        )

        if scenario_id is not None:
            query = query.filter(CustomParameter.scenario_id == scenario_id)

        return query.all()

    def __init__(self, model, *args, **kwargs):
        if not hasattr(model, '__parameterized__'):
            raise TypeError(f'{model.__qualname__} is not a parameterized model')
        self.__instance = model

    def get_own_parameter_definitions(self, name=None):
        entity = self.__instance

        dm_ids = [d.id for d in entity.domains]  # Relevant domain ids

        query = ParameterService.db.session.query(ParameterDefinition).join(
            ParameterDomain, ParameterDomain.id == ParameterDefinition.domain_id
        ).filter(
            ParameterDomain.id.in_(dm_ids)
        )

        if name is not None:
            query = query.filter(or_(
                ParameterDefinition.full_name == name,
                ParameterDefinition.variable_name == name
            ))

        return query.all()

    def get_own_custom_parameters(self, name=None, scenario=None, any_scenario=False):
        entity = self.__instance

        query = ParameterService.db.session.query(CustomParameter).join(
            ParameterDefinition, ParameterDefinition.id == CustomParameter.definition_id
        ).join(
            ParameterDomain, ParameterDomain.id == ParameterDefinition.domain_id
        )

        dm_ids = [d.id for d in entity.domains]  # Relevant domain ids

        if isinstance(entity, Scenario):
            query = query.filter(
                CustomParameter.scenario_id == entity.id,
                ParameterDomain.id.in_(dm_ids)
            )

        else:
            if (any_scenario or False):
                query = query.filter(
                    ParameterDomain.id.in_(dm_ids),
                    CustomParameter.requirements == f'(self.id == {entity.id})'
                )
            else:
                # Get the current Scenario id
                if scenario is None:
                    s_id = entity.current_scenario().id
                else:
                    s_id = scenario.id
                query = query.filter(
                    CustomParameter.scenario_id == s_id,
                    ParameterDomain.id.in_(dm_ids),
                    CustomParameter.requirements == f'(self.id == {entity.id})'
                )

        if name is not None:
            query = query.filter(or_(
                ParameterDefinition.full_name == name,
                ParameterDefinition.variable_name == name
            ))

        return query.all()


def matches_parameter_def(param, **kwargs):
    characteristics = get_parameter_characteristics(param)
    for k, v in characteristics.items():
        d_v = kwargs.get(k)
        if isinstance(v, str):
            v = strip_spaces(v)
        if isinstance(d_v, str):
            d_v = strip_spaces(d_v)
        if (v is None or v == '') and (d_v is None or d_v == ''):
            continue
        if v != d_v:
            return False
    return True


def get_parameter_characteristics(param):
    if isinstance(param, ParameterDefinition):
        return {
            'requirements': '',
            'value': param.default_value,
            'unit': param.default_unit,
            'formula': (
                None if not param.default_formula
                else param.default_formula.equation
            )
        }
    return {
        'requirements': param.requirements,
        'value': param.value,
        'unit': param.unit,
        'formula': (
            None if not param.formula
            else param.formula.equation
        )
    }


def get_or_create_custom_param(param_obj=None, kwargs={}, include_default_value = False, new_formula=False, no_commit=False):
    if isinstance(param_obj, CustomParameter):
        return param_obj
    
    elif isinstance(param_obj, ParameterDefinition):
        default_kwargs = {
            "definition_id": param_obj.id,
            "unit": param_obj.default_unit,
            "formula_id": param_obj.default_formula_id,
        }
        if include_default_value:
            default_kwargs["value"] = param_obj.default_value

        keys = set(list(kwargs.keys()) + list(default_kwargs.keys()))
        for key in keys:
            if key not in kwargs:
                kwargs[key] = default_kwargs[key]

    elif param_obj:
        raise Exception(f"Param type {type(param_obj)} not supported")

    if new_formula:
        default_param = ParameterService.definitions.get(kwargs["definition_id"])
        new_formula_obj = FormulaService.create(equation=default_param.default_formula.equation)
        kwargs["formula_id"] = new_formula_obj.id

    return ParameterService.get_or_create(**kwargs, no_commit=no_commit)


def update_custom_param_value(param_obj, val):
    if not isinstance(param_obj, CustomParameter):
        raise Exception(f"Param type {type(param_obj)} not supported")
    
    try:
        if param_obj.value != float(val):
            param_obj.value = val
            ParameterService.update(param_obj)
    except Exception as e:
        print(f"Could not convert value {val} to float: {e}")
        if param_obj.value != val:
            param_obj.value = val
            ParameterService.update(param_obj)

    return param_obj


def convert_unit(val, unit, strict=False):
    if not hasattr(val, 'dimensionality'):
        val = as_quantity(val, unit)
    else:
        if not strict and unit:
            val = val.magnitude
        try:
            val = as_quantity(val, unit)
        except Exception:
            # print('unit error (v) -', val)
            # print('unit error (u) -', unit)
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
        # val = CallableQuantity(val)
        return val
    return wrapped


def evaluate_parameter(
    param, entity, scenario=None,
    strict_units=False, default=None,
    **kwargs
):
    if (
        isinstance(param, ParameterDefinition)
        or isinstance(param, CustomParameter)
    ):
        unit = param.unit or ''
        q = param.quantity
        if isinstance(q, Formula):
            arguments = {}
            if 'self.' in q.equation:
                arguments['self'] = entity
            if 'environment.' in q.equation:
                if scenario is not None:
                    arguments['environment'] = scenario
                else:
                    arguments['environment'] = entity.current_scenario()
            arguments.update(kwargs)
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
        # val = CallableQuantity(val)
        return val
    return default


def parameterize(cls, globalize_custom_parameters=False, default_scenario=None):
    cls_name = cls.__name__
    globalize_custom_parameters = globalize_custom_parameters or False

    def get_scenario(obj, scenario: Scenario = None) -> Scenario | None:
        if scenario is not None:
            # CacheManager.clear_cache(f'entity_param::{cls_name}')
            setattr(obj, '__current_scenario', scenario)
        if getattr(obj, '__current_scenario', None) is None:
            s = None
            if default_scenario is not None:
                try:
                    s = default_scenario(obj)
                except Exception:
                    pass
            if s is None:
                from trim_db.services import ScenarioService
                s = ScenarioService.get_or_create(name='Default', creator_id=1)
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
    @CacheManager.with_caching(f'entity_domains')
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

    @CacheManager.with_caching('entity_param_dicts')
    def get_param_dict(entity):
        if entity == cls:
            # If called on the class
            # (e.g., Entity.parameters),
            # return all possible definitions
            return {
                pd.name: pd
                for d in sorted(
                    # Sort to make sure sub-domains override parents
                    entity.domains,
                    key=lambda x: len(str(x.requirements or ''))
                )
                for pd in d.parameter_definitions
            }
        else:
            # If called on an instance
            # (e.g., Entity().parameters),
            # return custom implementations of each definition,
            # or the definition itself if no specific version applies

            # Get definitions
            pds = ParameterService(entity).get_own_parameter_definitions()
            # Sort to make sure sub-domains override parents
            pds = list(sorted(  # We'll want subdomains LAST for these
                pds, key=lambda x: len(str(x.domain.requirements or ''))
            ))

            # Get custom implementations
            current_scenario = _get_current_scenario(entity)
            if globalize_custom_parameters:
                cps = ParameterService(entity).get_own_custom_parameters(
                    any_scenario=True
                )
            else:
                cps = ParameterService(entity).get_own_custom_parameters(
                    scenario=current_scenario
                )
            # Sort to make sure sub-domains override parents
            cps = list(reversed(sorted(  # We'll want subdomains FIRST for these
                cps, key=lambda x: len(str(x.definition.domain.requirements or ''))
            )))

            # Construct dict
            p = {pd.name: pd for pd in pds}
            cp_update = {}
            for cp in cps:
                pd_nm = cp.definition.name
                if pd_nm not in cp_update or cp.scenario_id == current_scenario.id:
                    cp_update[pd_nm] = cp
            p.update(cp_update)
            return p

    # A class that allows you to get/set parameter definitions
    # (both globally for the class and custom for an instance of the class)
    class ParameterManager:
        def __init__(self, entity):
            self.entity = entity
            self._default_domain = get_default_domain()

        @property
        def unit_registry(self):
            return ureg

        @property
        def _params(self):
            return get_param_dict(self.entity)

        def __len__(self):
            return len(self._params)

        def __contains__(self, key):
            return key in self._params

        def __getitem__(self, key):
            return self._params[key]

        def get(self, key, default=None):
            return self._params.get(key, default)

        def get_custom(self, key, default=None):
            param = self._params.get(key, default)
            if param is None or isinstance(param, ParameterDefinition):
                return default
            return param

        def __setitem__(self, key, value):
            raise NotImplementedError

        def add(
            self, name, domain=None,
            value=None, unit=None, formula=None,
            full_name=None, description=None,
            requirements=None, domain_name=None,
            force_update=False
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

            if self.entity != cls:
                if requirements:
                    requirements = f'({requirements}) and '
                requirements += f'(self.id == {self.entity.id})'

            existing = self.get(name)
            if self.entity != cls and isinstance(existing, ParameterDefinition):
                existing = None

            if existing and existing.domain == domain:
                if matches_parameter_def(
                    existing,
                    value=value, unit=unit, formula=formula,
                    requirements=requirements
                ):
                    # This parameter, with this exact definition,
                    # already exists!
                    return

                # Otherwise, check if we can reconcile
                # the existing definition and the new definition

                ex_chars = get_parameter_characteristics(existing)
                existing_formula = ex_chars['formula']

                if formula is not None and existing_formula is None:
                    # If the new definition has a formula
                    # where the old definition had a static value,
                    # check if the static value is the else condition
                    # of the new formula.
                    # If it is, that's ok, and we can clear the value
                    # and use the formula!
                    ex_val = existing.value
                    if ex_val is not None:
                        ex_val = str(ex_val)
                        was_number = ex_val.replace('.', '').isnumeric()
                        if was_number:
                            ex_val = float(ex_val)
                        if f'else {ex_val})' in formula:
                            ex_chars['value'] = value
                            existing.value = value
                        elif was_number:
                            ex_val = int(ex_val)
                            if f'else {ex_val})' in formula:
                                ex_chars['value'] = value
                                existing.value = value

                elif formula is None and existing_formula is not None:
                    # If the old definition had a formula
                    # where the new definition has a static value,
                    # check if the static value is the else condition
                    # of the old formula.
                    # If it is, that's ok, and we can clear the value
                    # and use the existing_formula!
                    new_val = value
                    if new_val is not None:
                        new_val = str(new_val)
                        is_number = new_val.replace('.', '').isnumeric()
                        if is_number:
                            new_val = float(new_val)
                        if f'else {new_val})' in existing_formula:
                            value = existing.value
                            formula = existing_formula
                        elif is_number:
                            new_val = int(new_val)
                            if f'else {new_val})' in existing_formula:
                                value = existing.value
                                formula = existing_formula

                merged = None
                # old = None
                # By passing existing_formula instead of formula,
                # we prove that if this is true then all the other
                # components must match
                if matches_parameter_def(
                    existing,
                    value=value, unit=unit, formula=existing_formula,
                    requirements=requirements
                ):
                    # Everything EXCEPT the formula matches!
                    # Maybe we can merge them?
                    try:
                        merged = merge_formulas(existing_formula, formula)
                    except Exception:
                        # We don't know how to merge these
                        import traceback
                        traceback.print_exc()
                        merged = None
                    if merged is not None:
                        # We figured out how to merge them!
                        formula = merged or formula

                new_def = {
                    'requirements': requirements,
                    'value': value,
                    'unit': unit,
                    'formula': formula
                }
                changelog = '<changelog>'
                for k, v in new_def.items():
                    old_v = ex_chars.get(k)
                    sym = '==' if v == old_v else '>>'
                    changelog += f'\n\t{k} : {old_v} {sym} {v}'
                changelog += '\n</changelog>'
                if merged is None:
                    # The new definition is incompatible with the existing one
                    if force_update or name == "Flushes":
                        # We're just going to overwrite the existing definition
                        print(
                            f'WARNING! Updating existing value:\n{changelog}'
                        )
                    else:
                        # We can't do this
                        raise AssertionError(
                            f'Trying to add incompatible definition for'
                            f' "{name}" ({domain.name}):\n{changelog}'
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

        def set(
            self, name, domain=None,
            value=None, unit=None, formula=None,
            full_name=None, description=None,
            requirements=None, domain_name=None
        ):
            return self.add(
                name, domain=domain,
                value=value, unit=unit, formula=formula,
                full_name=full_name, description=description,
                requirements=requirements, domain_name=domain_name,
                force_update=True
            )

        def keys(self):
            return self._params.keys()

        def values(self):
            return self._params.values()

        def items(self):
            return self._params.items()

        def evaluate(self, param, **kwargs):
            if self.entity == cls:
                raise TypeError('Cannot Evaluate Parameters at the Class Level')
            if isinstance(param, str):
                param = self.get(param)
            return evaluate_parameter(param, self.entity, **kwargs)

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

    NO_CUSTOM_GET = [
        'domains', 'parameters',
        '__current_scenario', 'current_scenario',
        '__parameterized__'
    ]

    # A method to get the VALUE of a parameter
    @CacheManager.with_caching(f'entity_param::{cls_name}')
    def get_parameter(
        entity, name, strict_units=False, default=NoneParameter.instance()
    ):
        # print(f'ENTITY IS {entity} name is {name} class_name {cls_name}')
        if name.startswith('_') or name in NO_CUSTOM_GET:
            return entity.__getattribute__(name)

        # This method of accessing parameters exists for legacy reasons,
        # so it only needs to work for code like "Entity().param_name".
        # Calling "Entity.param_name" is NOT supported
        param = entity.parameters.get(name, default)

        return evaluate_parameter(
            param,
            entity=entity,
            strict_units=strict_units,
            default=default
        )

    # Override getattr
    setattr(cls, '__getattr__', get_parameter)

    # Mark this model as parameterized
    setattr(cls, '__parameterized__', True)

    return cls
