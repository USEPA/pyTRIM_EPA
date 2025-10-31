
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
# '(3 if 4 else (1 if 2 else 0))'
# >>> merge_formulas('1 if 2 else 0', '1 if 4 else 0')
# '(1 if ((4) or (2)) else 0)'
# >>> merge_formulas('1 if 2 else 0', '1 if 4 else 3')
# '(1 if ((4) or (2)) else 3)'
# >>> merge_formulas('1 if a in {1,2,3} else 0', '2 if a in {4,5,6} else 0')
# '(2 if a in {4, 5, 6} else (1 if a in {1, 2, 3} else 0))'
# >>> merge_formulas('1 if a in {1,2,3} else 0', '1 if a in {4,5,6} else 0')
# '(1 if a in {1, 2, 3, 4, 5, 6} else 0)'
# >>> merge_formulas('1 if a in {1,2,3} else 0', '1 if a in {4,5,6} else 2')
# '(1 if a in {1, 2, 3, 4, 5, 6} else 2)'
# >>> merge_formulas('1 if a in {1,2,3} else 0', '2 if a in {3,4,5} else 0')
# '(2 if a in {3, 4, 5} else (1 if a in {1, 2} else 0))'
# >>> merge_formulas('1 if a in {1,2,3} else 0', '2 if a in {3,4,5} else 3')
# '(2 if a in {3, 4, 5} else (1 if a in {1, 2} else 3))'
def merge_formulas(f1, f2):
    if f1 is None:
        return f2
    if f2 is None:
        return f1

    if not (is_ternary(f1) and is_ternary(f2)):
        raise AssertionError('Can only merge ternary expressions!')

    merged = merge_ternaries([f1, f2])
    for val, conds in merged.items():
        restrung = []
        for c in conds:
            if c is None:
                restrung.append(c)
                continue
            s = c['element'] + ' ' + c['operator'] + ' '
            if c['operator'] == 'in':
                s += str(set(c['check_val']))
            else:
                s += str(c['check_val'])
            if 'negate' in c:
                s = 'not ' + s
            restrung.append(s.strip())
        merged[val] = restrung

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
        ordered_conds = order_condition_types(
            cond, ternary_condition_order, as_dict=True
        )
        for cond in ordered_conds.values():
            if not cond:
                continue
            cond = merge_conditions(cond)
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
    def strip_parens(s):
        while s.count('(') > s.count(')'):
            if not s.startswith('('):
                break
            s = s[1:]
        while s.count(')') > s.count('('):
            if not s.endswith(')'):
                break
            s = s[:-1]
        return s

    def de_paren(s):
        while s.startswith('(') and s.endswith(')'):
            s = s[1:-1]
        return s

    def split_value_from_condition(s):
        s = s.split(' if ')
        v = s[0]
        v = de_paren(v)
        if len(s) > 1:
            cond = s[1]
        else:
            cond = None
        if cond:
            cond = split_conditions(cond, 'or')
        return v, cond

    def pairwise(iterable):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        # https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
        a = iter(iterable)
        return zip(a, a)

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

    condition_checks = ['==', 'is', 'in', '!=', '<', '>', '<=', '>=']

    def parse_condition(condition):
        if condition is None:
            return condition
        condition = f' {condition} '

        for op in ['or', 'and']:
            if f' {op} ' in condition:
                return [parse_condition(x) for x in split_conditions(condition, op)]

        negate = False
        if 'not' in condition:
            negate = True
            condition = de_paren(condition.replace(f' not ', ' '))
        check = None
        for c in condition_checks:
            if f' {c} ' in condition:
                check = c
                break
        if check is None:
            check = ''  # We don't know how to split this
            condition = [condition, '']
        else:
            condition = [de_paren(x) for x in condition.split(f' {check} ')]

        parsed = []
        for el, check_val in pairwise(condition):
            check_val = check_val.strip()
            if check_val != '' and check_val[0] in '{[' and check_val[-1] in ']}':
                check_val = [parse_val(x) for x in check_val[1:-1].split(',')]
            else:
                check_val = parse_val(check_val)
            x = {
                'element': el.strip(),
                'operator': check,
                'check_val': check_val
            }
            if negate:
                x['negate'] = True
            parsed.append(x)
        return parsed

    f = formula.split(' else ')
    cases = {}
    for s in f:
        s = strip_parens(s)
        v, cond = split_value_from_condition(s)
        if not isinstance(cond, list):
            cond = [cond]
        parsed = []
        for x in (parse_condition(c) for c in cond):
            if isinstance(x, list):
                parsed.extend(x)
            else:
                parsed.append(x)
        cases.setdefault(v, []).extend(parsed)
    return cases


def split_conditions(full_condition, operator):
    operator = f' {operator} '
    if operator not in full_condition:
        return full_condition
    parts = []
    for x in full_condition.split(operator):
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


def merge_ternaries(ternaries):
    inverted = {}

    while len(ternaries):
        tern = break_down_ternary(ternaries.pop())

        for val, conditions in tern.items():
            for cond in conditions:
                if cond is None:
                    # this is a default (i.e., the final "else")
                    if None not in inverted:
                        inverted[None] = val
                    continue
                op = cond['operator']
                el = cond['element']
                check = cond['check_val']
                neg = cond.get('negate') or False

                if el not in inverted:
                    inverted[el] = {}

                if op not in inverted[el]:
                    inverted[el][op] = {}
                    if op == 'in':
                        inverted[el][op] = {
                            c: {'negate': neg, 'value': val}
                            for c in check
                        }
                    else:
                        inverted[el][op][check] = {'negate': neg, 'value': val}

                else:
                    existing = inverted[el][op]
                    if op == 'in':
                        for c in check:
                            if c not in existing:
                                existing[c] = {'negate': neg, 'value': val}
                    else:
                        if check not in existing:
                            existing[check] = {'negate': neg, 'value': val}

    merged = {}

    for el, ops in inverted.items():
        if el is None:
            merged[ops] = [None]
            continue
        for op, check_vals in ops.items():
            for check, val in check_vals.items():
                neg = val['negate']
                val = val['value']
                if val not in merged:
                    merged[val] = []
                cond = None
                if op == 'in':
                    cond = [
                        c for c in merged[val]
                        if (
                            c['element'] == el
                            and c['operator'] == op
                            and (c.get('negate') or False) == neg
                        )
                    ]
                    cond = cond[0] if cond else None
                if cond is None:
                    cond = {
                        'element': el,
                        'operator': op
                    }
                    merged[val].append(cond)
                if op == 'in':
                    if 'check_val' not in cond:
                        cond['check_val'] = []
                    cond['check_val'].append(check)
                else:
                    cond['check_val'] = check

                if neg:
                    cond['negate'] = True

    return merged

