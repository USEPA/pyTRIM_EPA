from ..schema.scenarios.models import Scenario
from ..schema.parameters.models import *
from ..schema.parameters.utils import as_quantity, NoneParameter
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

    @classmethod
    def commit(cls):
        super().commit()
        CacheManager.clear_cache(f'entity_param_dicts')

    class domains(GenericService):
        __model__ = ParameterDomain

    class definitions(GenericService):
        __model__ = ParameterDefinition


class classproperty:
    def __init__(self, f):
        self._f = f

    def __get__(self, obj, owner):
        return self._f(owner, obj)


# class CallableQuantity():
#     def __init__(self, quantity):
#         self.__quantity__ = quantity

#     def __getattr__(self, name):
#         if name == '__quantity__':
#             raise AttributeError()
#         return getattr(self.__quantity__, name)

#     def __call__(self, *args, **kwargs):
#         return self.__quantity__

#     def __repr__(self, *args, **kwargs):
#         return self.__quantity__.__repr__(*args, **kwargs)

#     def __str__(self, *args, **kwargs):
#         return self.__quantity__.__str__(*args, **kwargs)


def strip_spaces(s):
    return ''.join(s.split(' '))


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


def merge_formulas(f1, f2):
    if f1 is None:
        return f2
    if f2 is None:
        return f1

    def is_ternary(formula):
        if ' if ' not in formula:
            return False
        if ' else ' not in formula:
            return False
        # Contains a ternary ... but is the ternary at the ROOT?
        check = formula.split(' if ')
        if '(' in check[0] and check[0].split('(')[0].strip():
            # Something was before the ternary (e.g., "2 * (1 if False else 0)")
            return False
        check = formula.split(' else ')
        if ')' in check[-1] and check[-1].split(')')[-1].strip():
            # Something was after the ternary (e.g., "(1 if False else 0) * 2")
            return False
        # Looks like the root was a ternary!
        return True

    def break_down_ternary(formula):
        def split_or_conditions(cond):
            if ' or ' not in cond:
                return cond
            parts = []
            for x in cond.split(' or '):
                while x.count('(') > x.count(')'):
                    if not x.startswith('('):
                        return cond  # Unable to break this down
                    x = x[1:]
                while x.count(')') > x.count('('):
                    if not x.endswith(')'):
                        return cond  # Unable to break this down
                    x = x[:-1]
                parts.append(x)
            return parts

        f = formula.split(' else ')
        cases = {}
        for s in f:
            while s.count('(') > s.count(')'):
                if not s.startswith('('):
                    break
                s = s[1:]
            while s.count(')') > s.count('('):
                if not s.endswith(')'):
                    break
                s = s[:-1]
            s = s.split(' if ')
            v = s[0]
            while v.startswith('(') and v.endswith(')'):
                v = v[1:-1]
            if len(s) > 1:
                cond = s[1]
            else:
                cond = None
            if cond:
                cond = split_or_conditions(cond)
            if not isinstance(cond, list):
                cond = [cond]
            cases.setdefault(v, []).extend(cond)
        return cases

    def merge_conditions(conditions):
        def parse_val(v):
            v = v.strip()
            try:
                v = int(v)
            except ValueError:
                try:
                    v = float(v)
                except ValueError:
                    pass
            return v

        merged_conditions = []
        check_in = {}
        for cond in conditions:
            while cond[0] in '(' and cond[-1] in ')':
                cond = cond[1:-1]
            c = cond.split(' in ')
            if len(c) != 2:
                merged_conditions.append(cond)
                continue
            expression = c[0]
            contained_by = c[1]
            if not ((contained_by[0] in '{[') and (contained_by[-1] in ']}')):
                merged_conditions.append(cond)
                continue
            contained_by = contained_by[1:-1]
            contained_by = [parse_val(x) for x in contained_by.split(',')]
            check_in.setdefault(expression, []).extend(contained_by)
        for k, v in check_in.items():
            merged_conditions.append(f'{k} in {set(v)}')
        return merged_conditions

    if not (is_ternary(f1) and is_ternary(f2)):
        raise AssertionError('Can only merge ternary expressions!')

    f1 = break_down_ternary(f1)
    f2 = break_down_ternary(f2)

    merged = {}
    for k, v in f1.items():
        merged[k] = []
        merged[k].extend(v)
    for k, v in f2.items():
        merged.setdefault(k, [])
        for x in v:
            if x in merged[k]:
                continue
            merged[k].append(x)

    merged_ternary = []
    default = None
    for v, cond in merged.items():
        if None in cond:
            default = v
            cond = [x for x in cond if x is not None]
        if not cond:
            continue
        old = cond
        cond = merge_conditions(cond)
        if len(cond) > 1:
            cond = '((' + ') or ('.join(cond) + '))'
        else:
            cond = cond[0]
        merged_ternary.append(f'{v} if {cond} else')

    # Make sure ternaries are ordered so that more specific conditions
    # are hit first, if possible (i.e., object id > media id > other)
    cond_types = {'id': [], 'media': [], 'other': []}
    for x in merged_ternary:
        if '.media.id' in x:
            cond_types['media'].append(x)
        elif '.id' in x:
            cond_types['id'].append(x)
        else:
            cond_types['other'].append(x)
    merged_ternary = (
        cond_types['id'] + cond_types['media'] + cond_types['other']
    )

    merged = '(' + ' ('.join(merged_ternary) + f' {default}' + ')'
    while merged.count(')') < merged.count('('):
        merged += ')'

    return merged


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


def parameterize(cls, default_scenario=None):
    cls_name = cls.__name__

    def get_scenario(obj, scenario=None):
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

    @CacheManager.with_caching(f'entity_param_dicts')
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
            # or the definition itself
            # if no specific version applies
            p = {}
            got_custom = {}
            s_id = _get_current_scenario(entity).id
            for d in sorted(
                # Sort to make sure sub-domains override parents
                entity.domains,
                key=lambda x: len(str(x.requirements or ''))
            ):
                for pd in d.parameter_definitions:
                    if pd.name not in got_custom:
                        # If a higher domain had a custom parameter
                        # for this entity, don't overwrite it with
                        # the default for this subdomain;
                        # only custom parameters should overwrite
                        # custom parameters
                        p[pd.name] = pd
                    for cp in pd.instances:
                        # FIXME need to either correct the chem param definitions 
                        # or init custom params for each new scenario.
                        # at the moment chemicals take custom params from the Foundries/Default scenario
                        if cp.scenario_id != s_id and entity.__tablename__ != 'chemical':
                            continue
                        if cp.validate(entity):
                            got_custom[pd.name] = True
                            p[pd.name] = cp
                            break
            return p

    # A class that allows you to get/set parameter definitions
    # (both globally for the class and custom for an instance of the class)
    class ParameterManager:
        def __init__(self, entity):
            self.entity = entity
            self._default_domain = get_default_domain()

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

        def __setitem__(self, key, value):
            raise NotImplementedError

        def add(
            self, name, domain=None,
            value=None, unit=None, formula=None,
            full_name=None, description=None,
            requirements=None, domain_name=None,
            force_update=False
        ):
            # if (
            #     str(formula).endswith('.Volume')
            #     or '.Volume ' in str(formula)
            #     or '.Volume)' in str(formula)
            # ):
            #     raise AssertionError(formula)
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
                old = None
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
                    except Exception as e:
                        # We don't know how to merge these
                        import traceback
                        traceback.print_exc()
                        merged = None
                    if merged is not None:
                        # We figured out how to merge them!
                        old = formula
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
                changelog +='\n</changelog>'
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
            # val = CallableQuantity(val)
            return val
        return wrapped

    # A method to get the VALUE of a parameter
    @CacheManager.with_caching(f'entity_param::{cls_name}')
    def get_parameter(
        entity, name, strict_units=False, default=NoneParameter.instance()
    ):
        # print(f'ENTITY IS {entity} name is {name} class_name {cls_name}')
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
            # val = CallableQuantity(val)
            return val
        return default

    # Override getattr
    setattr(cls, '__getattr__', get_parameter)

    return cls
