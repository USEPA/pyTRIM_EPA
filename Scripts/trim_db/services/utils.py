
class classproperty:
    def __init__(self, f):
        self._f = f

    def __get__(self, obj, owner):
        try:
            return self._f(owner, obj)
        except Exception as e:
            if 'takes 1 positional argument' in str(e):
                return self._f(owner)
            raise

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


# EXAMPLES of merge_formulas:
# >>> merge_formulas('1 if 2 else 0', '3 if 4 else 0')
# '(1 if 2 else (3 if 4 else 0))'
# >>> merge_formulas('1 if 2 else 0', '1 if 4 else 0')
# '(1 if ((2) or (4)) else 0)'
# >>> merge_formulas('1 if 2 else 0', '1 if 4 else 3')
# '(1 if ((2) or (4)) else 3)'
# >>> merge_formulas('1 if a in {1,2,3} else 0', '2 if a in {4,5,6} else 0')
# '(1 if a in {1, 2, 3} else (2 if a in {4, 5, 6} else 0))'
# >>> merge_formulas('1 if a in {1,2,3} else 0', '1 if a in {4,5,6} else 0')
# '(1 if a in {1, 2, 3, 4, 5, 6} else 0)'
# >>> merge_formulas('1 if a in {1,2,3} else 0', '1 if a in {4,5,6} else 2')
# '(1 if a in {1, 2, 3, 4, 5, 6} else 2)'
def merge_formulas(f1, f2):
    if f1 is None:
        return f2
    if f2 is None:
        return f1

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

    # Make sure ternaries are ordered so that more specific conditions
    # are hit first, if possible (i.e., object id > media id > other)
    ternary_condition_order = ['.id', '.media.id']

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
        ordered_conds = order_condition_types(
            cond, ternary_condition_order, as_dict=True
        )
        for cond in ordered_conds.values():
            if not cond:
                continue
            if len(cond) > 1:
                cond = '((' + ') or ('.join(cond) + '))'
            else:
                cond = cond[0]
            merged_ternary.append(f'{v} if {cond} else')

    merged_ternary = order_condition_types(
        merged_ternary, ternary_condition_order
    )

    merged = '(' + ' ('.join(merged_ternary) + f' {default}' + ')'
    while merged.count(')') < merged.count('('):
        merged += ')'

    return merged


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


def split_or_conditions(full_condition):
    if ' or ' not in full_condition:
        return full_condition
    parts = []
    for x in full_condition.split(' or '):
        while x.count('(') > x.count(')'):
            if not x.startswith('('):
                return full_condition  # Unable to break this down
            x = x[1:]
        while x.count(')') > x.count('('):
            if not x.endswith(')'):
                return full_condition  # Unable to break this down
            x = x[:-1]
        parts.append(x)
    return parts


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


def order_condition_types(conditions, condition_checks, as_dict=False):
    OTHER_TYPE = '__other__'

    cond_types = {x: [] for x in condition_checks}
    cond_types[OTHER_TYPE] = []

    for x in conditions:
        checks = x.split(' or ')  # split into sub-conditions
        had_x_condition = {txt: False for txt in condition_checks}
        for check in checks:
            for txt in reversed(sorted(
                condition_checks, key=lambda s: len(s)
            )):
                if txt in check:
                    had_x_condition[txt] = True
                    break
        for txt in condition_checks:
            if had_x_condition[txt]:
                cond_types[txt].append(x)
                break
        else:
            cond_types[OTHER_TYPE].append(x)

    if as_dict:
        return cond_types

    ordered_conditions = []
    for x in cond_types:
        ordered_conditions += cond_types[x]
    return ordered_conditions
