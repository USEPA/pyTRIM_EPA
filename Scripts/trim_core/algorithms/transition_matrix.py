import os
import pandas as pd
import numpy as np
from trim_db.schema import *
from trim_db.schema.parameters.equations import evaluated_args, \
    evaluator, NoEval
from trim_db.services import *

__all__ = ['make_transition_matrix']

DEBUG = os.getenv('DEBUG_TRANSITION_MATRIX')
RESTRICT_COMPARTMENTS = [
    x.strip()
    for x in str(os.getenv('TRANSITION_MATRIX_COMPARTMENTS', '')).split(',')
    if x.strip()
]


def is_compartment_of_interest(comp):
    if not RESTRICT_COMPARTMENTS:
        return True
    for x in RESTRICT_COMPARTMENTS:
        if x in comp.standard_name:
            return True
    return False


def make_transition_matrix(scenario):
    chem_list = list(sorted(
        scenario.chemicals, key=lambda x: x.name
    ))
    comp_list = list(sorted(
        scenario.compartments, key=lambda x: x.standard_name
    ))

    if DEBUG:
        comp_list = [x for x in comp_list if is_compartment_of_interest(x)]

    n_chem = len(chem_list)
    n_comp = len(comp_list)

    matrix_dimensions = n_chem * n_comp

    source_matrix = np.zeros(matrix_dimensions, dtype=float)
    transition_matrix = np.zeros(
        (matrix_dimensions, matrix_dimensions), dtype=float
    )

    index_names = ['' for _ in source_matrix]

    chem_indices = {
        c: i for i, c in enumerate(chem_list)
    }

    try:
        for chem_idx, chem in enumerate(chem_list):
            # if chem.name != 'Elemental Mercury':
            #     continue
            print('\n' + '==' * 28)
            print(f'Chemical = {chem.name}')
            print('==' * 28)

            for x, sender in enumerate(comp_list):
                tm_x = int(chem_idx * n_comp + x)

                index_names[tm_x] = chem.name + '_' + sender.standard_name

                try:
                    dr = sender.deposition_rate(chemical=chem)
                    source_matrix[tm_x] += dr
                except Exception:
                    pass

                # Some media just don't send anything
                if not sender.media.can_emit:
                    continue

                for y, receiver in enumerate(comp_list):
                    # Some media just don't receive anything
                    if not receiver.media.can_absorb:
                        continue

                    # print(sender.standard_name, '>', receiver.standard_name)

                    links = sender.get_links(receiver)
                    if not links:
                        continue

                    tm_y = int(chem_idx * n_comp + y)

                    print_vals = []
                    print_vals.append(
                        f'\n\t{sender.standard_name} >'
                        f' {receiver.standard_name}'
                        f' ({chem_idx + 1}/{n_chem},'
                        f' {x + 1}/{n_comp}, {y + 1}/{n_comp})'
                    )
                    # print_vals.append(links)

                    for link in links:
                        # print(link)
                        for transport_proc in link.transport_processes(chem):
                            # print('\t', transport_proc.name)
                            check_alg = False
                            transfer_factor = np.nan
                            try:
                                transfer_factor = transport_proc.eval(
                                    sender=sender, receiver=receiver,
                                    chemical=chem,
                                    environment=scenario
                                )
                            except:
                                print_vals.append(f'Unable to evaluate {transport_proc.name}')
                                check_alg = True
                            # print('\t\ttf =', transfer_factor)
                            try:
                                transfer_factor = transfer_factor.magnitude
                            except Exception:
                                pass
                            print_vals.append(
                                f'\t\t- "{transport_proc.name}"'
                                f' = {transfer_factor}'
                            )

                            try:
                                if pd.isna(transfer_factor):
                                    print_vals.append('\t\t\t Unexpected NAN!')
                                    print_vals.extend([
                                        f'\t\t\t {s}'
                                        for s in check_alg_values(
                                            scenario, chem,
                                            transport_proc.name,
                                            sender.standard_name,
                                            receiver.standard_name
                                        )
                                    ])
                                    continue  # No point in continuing
                                elif not transfer_factor:
                                    continue  # No point in continuing
                            except ValueError:
                                print_vals.extend('\t\t\t Value error!')
                                check_alg = True
                                pass

                            if transport_proc.is_transform:
                                try:
                                    real_chem_idx = chem_indices[
                                        transport_proc.output_chemical
                                    ]
                                except KeyError:
                                    real_chem_idx = -1
                                if real_chem_idx < 0:
                                    tm_y = -1
                                else:
                                    tm_y = int(real_chem_idx * n_comp + x)

                            try:
                                transition_matrix[tm_x][tm_x] -= transfer_factor
                                if tm_y > -1:
                                    transition_matrix[tm_y][tm_x] += (
                                        transfer_factor
                                    )
                            except Exception:
                                print_vals.extend(
                                    '\t\t\t Error updating transfer matrix!'
                                )
                                check_alg = True
                            if check_alg:
                                print_vals.extend([
                                    f'\t\t\t {s}'
                                    for s in check_alg_values(
                                        scenario, chem,
                                        transport_proc.name,
                                        sender.standard_name,
                                        receiver.standard_name
                                    )
                                ])

                    if len(print_vals) > 1:
                        for ln in print_vals:
                            print(ln)

    except KeyboardInterrupt:
        pass

    df_tm = pd.DataFrame(
        transition_matrix, index=index_names,
        columns=index_names
    )
    df_sm = pd.DataFrame(
        source_matrix, index=index_names,
        columns=['deposition_rate_g_day-1']
    )

    return df_tm, df_sm


def check_alg_values(scenario, chemical, alg, sender, receiver):
    print_vals = []

    print_vals.append('')
    print_vals.append(alg)

    sender = scenario.get_compartment(sender)
    print_vals.append(f'sender = {sender}')
    print_vals.append(f'sender.media.id = {sender.media.id}')
    receiver = scenario.get_compartment(receiver)
    print_vals.append(f'receiver = {receiver}')
    print_vals.append(f'receiver.media.id = {receiver.media.id}')

    print_vals.append('')
    print_vals.append(f'sender.get_links(receiver) = {sender.get_links(receiver)}')

    process = TransportProcessService.get(name=alg)

    applies = process.applies_to(
        sender=sender, receiver=receiver,
        chemical=chemical
    )
    print_vals.append(f'transport_process_applies = {applies}')

    print_vals.extend(print_args(
        process.algorithm.equation, evaluator, new_names={
            'sender': sender,
            'receiver': receiver,
            'chemical': chemical,
            'environment': scenario
        }
    ))

    try:
        transfer_factor = process.eval(
            sender=sender, receiver=receiver,
            chemical=chemical,
            environment=scenario
        )
        print_vals.append(
            f'transfer_factor = {transfer_factor}'
        )
    except TypeError as e:
        if 'Invalid arguments for "' not in str(e):
            raise
        print_vals.append('Cannot evaluate transfer_factor')
    print_vals.append('')
    return print_vals


def print_args(equation, evaluator, new_names={}, depth=0):
    print_vals = []
    print_vals.append('')
    print_vals.append('--' * 15)
    print_vals.append(equation)
    print_vals.append('--' * 15)
    old_names = dict(evaluator.names)
    evaluator.names.update(new_names)
    try:
        eval_args = evaluated_args(equation, evaluator)
        for k in sorted(eval_args.keys()):
            if k in evaluator.names:
                continue
            v = eval_args[k]
            if str(v).startswith('<function '):
                continue
            if str(v).startswith('<bound method '):
                continue

            print_vals.append(f'{k} = {v}')
            continue
            if not isinstance(v, NoEval):
                print_vals.append(f'{k} = {v}')
            else:
                param = k.rsplit('.', 1)
                if len(param) != 2:
                    print_vals.append(f'{k} = {v} (<None>)')
                    continue
                obj = param[0]
                obj = obj.split('.', 1)
                obj[0] = f'evaluator.names.get("{obj[0]}")'
                # print_vals.append('.'.join(obj))
                try:
                    obj = eval('.'.join(obj))
                except Exception as e:
                    print_vals.append(f'{k} = {v} ({e})')
                    continue
                if obj is None:
                    print_vals.append(f'{k} = {v} (<None>)')
                    continue
                param = param[1]
                if '(' in param:
                    param = param.split('(')
                    args = param[1]
                    param = param[0]
                    args = [
                        x.strip()
                        for x in args.replace(')', '').split(',')
                    ]
                else:
                    args = []
                param = obj.parameters.get(param)
                if param is None:
                    print_vals.append(f'{k} = {v} (<None>)')
                    continue
                # print_vals.append(f'{k} = {param}({", ".join(args)})')
                try:
                    param.quantity
                except AttributeError:
                    print_vals.append(
                        f'\t-> {k} = {param} has no quantity'
                    )
                try:
                    print_vals.append(
                        f'\t-> Evaluating {k} = {param}'
                    )
                    print_vals.extend(print_args(
                        param.quantity.equation, evaluator,
                        new_names={
                            'self': obj,
                            **{
                                x: eval(x) for x in args
                            }
                        },
                        depth=(depth + 1)
                    ))
                except AttributeError:
                    print_vals.append(
                        f'\t-> {k} = {param.quantity} is not an equation'
                    )
    finally:
        evaluator.names = old_names
    print_vals.append('--' * 15)
    # print(print_vals)
    print_vals = [('\t' * depth) + s for s in print_vals]
    return print_vals
