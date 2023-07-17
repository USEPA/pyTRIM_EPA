import math
from simpleeval import EvalWithCompoundTypes
from trim_db.utils import iter_by_longest_key
from ..utils.caching import CacheManager
from .utils import is_number, UREG_CUSTOM_OPERATORS, UREG_CUSTOM_FUNCTIONS

__all__ = ['as_function', 'find_arguments', 'deconstruct_equation']


evaluator = EvalWithCompoundTypes(
    operators=UREG_CUSTOM_OPERATORS,
    names={
        'True': True, 'False': False,
        'None': None,
        'math': math
    },
    functions=UREG_CUSTOM_FUNCTIONS
)


def as_function(equation, with_caching=True, **default_kwargs):
    def get_prop(obj, prop_path):
        prop_path = prop_path.split('.')
        prop = obj
        for p in prop_path:
            prop = getattr(prop, p, None)
            if prop is None:
                break
        return prop

    arg_map = {}
    for element in find_arguments(equation):
        argname = element.split('.', 1)[0]

        arg = default_kwargs.get(argname)
        if not arg:
            continue

        if '.' in element:
            arg = get_prop(arg, element.split('.', 1)[-1])

        arg_map[element] = arg

    for arg in list(arg_map):
        if '.' not in arg:
            continue
        new_arg = arg.replace('.', '___')
        equation = equation.replace(arg, new_arg)
        arg_map[new_arg] = arg_map[arg]

    arg_map = {k: v for k, v in arg_map.items() if '.' not in k}

    equation = equation.replace('math.exp', 'safe_exp')
    equation = equation.replace('math.log', 'safe_log')
    equation = equation.replace('math.log10', 'safe_log10')
    equation = equation.replace('math.sqrt', 'safe_sqrt')

    def fix_non_callables(eq, evaluator):
        args = evaluated_args(eq, evaluator)
        for k, v in args.items():
            if not v == CANT_EVAL or not k.endswith(')'):
                continue
            non_func = k.rsplit('(')[0]
            if non_func not in args:
                continue
            eq = eq.replace(k, non_func)
        return eq

    @CacheManager.with_caching(f'equation::"{equation}"')
    def func(**kwargs):
        custom_arg_map = dict(arg_map)
        custom_arg_map.update(dict(kwargs))
        old_names = dict(evaluator.names)

        def str_with_args(eq, evaluator=None):
            # Replace longest keys first to avoid substring issues
            str_eq = {}
            for k, v in iter_by_longest_key(custom_arg_map):
                str_eq[k] = f'\t > {k} = {v}'

            if evaluator is not None:
                for k, v in evaluated_args(eq, evaluator).items():
                    if k in str_eq:
                        continue
                    str_eq[k] = f'\t > {k} = {v}'

            return '\n'.join([f'"{eq}"'] + [
                str_eq[k] for k in sorted(str_eq)
            ])

        try:
            evaluator.names.update(custom_arg_map)
            try:
                return evaluator.eval(equation)
            except TypeError as e:
                if 'is not callable' not in str(e):
                    raise
                return evaluator.eval(
                    fix_non_callables(equation, evaluator)
                )
                # raise
        except (IndexError):
            raise TypeError(
                f'Invalid index!'
                f'\n{str_with_args(equation, evaluator)}'
            )
        except Exception:
            print(f'{20 * "%%%%%%"}\n{evaluator.names}')
            print(f'{20 * "******"}\n{custom_arg_map}')
            print(f'{20 * "^^^^^^"}\n{equation}')
            print(f'{20 * "______"}')
            raise TypeError(
                f'Invalid equation!'
                f'\n{str_with_args(equation, evaluator)}'
            )
        finally:
            evaluator.names = old_names

    return func


CANT_EVAL = '<Unable to Evaluate>'


def evaluated_args(eq, evaluator=evaluator):
    full_args = find_arguments(eq, drop_functions=False)

    evaluated_args = {}
    for el in full_args:
        if '.to(' in el:
            el = el.rsplit('.to(', 1)[0]

        k = el
        if k.endswith('('):
            k = k[:-1]
        elif k.endswith(')'):
            k = k.rsplit('(', 1)[0]
        if k in evaluated_args:
            evaluated_args[el] = evaluated_args[k]
            continue

        if el.endswith('('):
            els = []
            for x in eq.split(el)[1:]:
                # x = x.split(')')[0]
                t = x.split(')')[0]
                p_i = 0
                while t.count("(") > t.count(")"):
                    p_i += 1
                    t = "".join(x.split(")")[:p_i]) + ")"
                x = t
                els.append(f'{el}{x})')
        elif el.endswith(')'):
            els = []
            el = el.rsplit('(', 1)[0] + '('
            for x in eq.split(el)[1:]:
                x = x.split(')')[0]
                els.append(f'{el}{x})')
        else:
            els = [el]

        for el in els:
            try:
                v = evaluator.eval(el)
            except Exception as err:
                print(err)
                v = CANT_EVAL
                try:
                    evaluated_args[k] = evaluator.eval(k)
                except Exception as err:
                    print(f"Problem evaluating {k}: {err}")
                    pass
            evaluated_args[el] = v
    return evaluated_args


RESERVED_WORDS = [
    'for', 'in', 'if', 'elif', 'else', 'not', 'and', 'or',
    'None', 'True', 'False',
    'math', 'min', 'max', '**'
]
OPERATORS = '+-*/=!<>?,'
OPEN_BRACKETS = '({['
CLOSE_BRACKETS = ')}]'


def is_reserved(s, base=False):
    if base:
        return s.split('.')[0] in RESERVED_WORDS
    return s in RESERVED_WORDS


def deconstruct_equation(equation):

    temp = equation

    for char in (OPERATORS + OPEN_BRACKETS + CLOSE_BRACKETS):
        temp = temp.replace(char, f' {char} ')

    temp = temp.split()

    def merge_last_n(array, n, merge_with=''):
        last_n = array[-n:]
        array = array[:-n]
        array.append(merge_with.join(last_n))
        return array

    deconstructed = []
    for el in temp:
        deconstructed.append(el)
        if len(deconstructed) == 1:
            continue

        prev = deconstructed[-2]

        if prev == '=' and el != "=":
            # this must be a sub-argument;
            # remove as distinct element and join to argname,
            # infixing equals sign as well
            deconstructed = deconstructed[:-2]
            deconstructed[-1] += '=' + el
            continue

        prev_op = prev in OPERATORS
        prev_reserved = is_reserved(prev)

        if (
            prev.endswith('e-') and is_number(prev[:-2])
            and is_number(el)
        ):
            # remove as distinct element and append to last
            deconstructed = merge_last_n(deconstructed, 2)
        elif (
            prev.endswith('e') and is_number(prev[:-1])
            and (el == '-' or is_number(el))
        ):
            # remove as distinct element and append to last
            deconstructed = merge_last_n(deconstructed, 2)

        elif el in '([':
            if not (prev_op or prev_reserved):
                # remove as distinct element and append to last
                deconstructed = merge_last_n(deconstructed, 2)
        elif el in OPERATORS:
            if prev_op:
                # remove as distinct element and append to last
                deconstructed = merge_last_n(deconstructed, 2)

    return [x.strip() for x in deconstructed if x.strip()]


def find_arguments(equation, combine_partial_args=True, drop_functions=True):
    deconstructed = deconstruct_equation(str(equation))

    def reconstruct_argument(element, i, deconstructed):
        if not element:
            return element
        while True:
            if i == 0:
                break
            i -= 1
            if is_reserved(deconstructed[i], base=True):
                break
            if element[0] in '.]':
                element = deconstructed[i] + element
            elif deconstructed[i][-1] in '][':
                element = deconstructed[i] + element
            elif i > 0 and deconstructed[i - 1][-1] in '[(':
                if is_reserved(deconstructed[i - 1], base=True):
                    break
                element = deconstructed[i - 1] + deconstructed[i] + element
                i -= 1
            else:
                break
        while element.startswith('('):
            element = element[1:]
        while element.count(')') > element.count('('):
            if not element.endswith(')'):
                break
            element = element[:-1]
        if (
            not element.endswith(')')
            and element.count('(') > element.count(')')
        ):
            element += ')'
        if element[0] == "-":
            element = element[1:]

        return element

    args = {}
    for i, element in enumerate(deconstructed):
        check = element.replace('.', '').replace('_', '').replace('(', '')
        check = check.strip()
        if not check.isalnum():
            continue

        if is_number(check):
            continue

        if is_reserved(check) or is_reserved(element.split('.')[0]):
            continue

        if drop_functions and element.endswith('('):
            element = element.rsplit('.', 1)[0]

        if not element:
            continue

        if element.endswith('.to('):
            element = element[:-4]

        if not element:
            continue

        if element.endswith('.magnitude'):
            element = element[:-10]

        if not element:
            continue

        if element[0] != '.' or not combine_partial_args:
            args[element] = 1

        if not combine_partial_args:
            continue

        element = reconstruct_argument(element, i, deconstructed)
        if element in args or not element:
            continue

        if drop_functions and element.endswith(')'):
            element = element.rsplit('(', 1)[0].rsplit('.', 1)[0]

        if not element:
            continue

        if element.endswith('()') and element not in equation:
            element = element[:-2]

            if element.endswith('.to'):
                element = element[:-3]

        if not element:
            continue

        args[element] = 1

    for k in list(args):
        for x in list(args):
            if x == k:
                continue
            if x.startswith(k):
                if k.endswith('(') or x[len(k):][0] == '(':
                    args.pop(k, None)
                    break

    return [x for x in sorted(args)]
