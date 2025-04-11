from ..services import TransportProcessService, FormulaService, \
    ChemicalService, CompartmentService
from ..schema.parameters.equations import deconstruct_equation
from .config import MEDIA_MAP

__all__ = ['parse_transport_processes']


def parse_transport_processes(algorithm_parameters, restrict_to=None):
    print(f'Loading algorithms from library data ...')

    def get_param(params, name, default=None):
        if name not in params:
            n = name.lower()
            for k in params:
                if k.lower() == n:
                    name = k
                    break
        return params.get(name, {}).get('value', default)

    def get_equation(params):
        equation = str(get_param(params, 'transferFactor', ''))
        if not equation:
            return None

        base_name = 'algorithm.'
        while base_name in equation:
            eq = deconstruct_equation(equation)
            for arg in sorted(eq, key=lambda x: -len(x)):
                if not arg.startswith(base_name):
                    continue
                prop = get_param(params, arg[len(base_name):])
                if not prop:
                    continue
                equation = equation.replace(arg, f'({prop})')

        return equation

    for m in MEDIA_MAP.values():
        CompartmentService.media.get_or_create(category=m)

    for name, params in algorithm_parameters.items():
        if restrict_to and name not in restrict_to:
            continue

        equation = get_equation(params)
        if not equation:
            continue

        proc = TransportProcessService.get_or_create(
            name=name, no_commit=True
        )

        if str(get_param(params, 'doesTransformChemical')).lower() == 'true':
            proc.category = 'Transform'
            chem = ChemicalService.get(
                name=get_param(params, 'receivingChemicalName')
            )
            proc.output_chemical = chem
        else:
            proc.category = 'Transport'

        cat = get_param(params, 'category')
        if cat and proc.category not in cat:
            proc.category += f'|{cat}'

        if proc.algorithm is None or proc.algorithm.equation != equation:
            f = FormulaService.create(equation=equation, no_commit=True)
            proc.algorithm = f

        requirements = []

        # print(name)
        try:
            sending_chem = ChemicalService.get(
                name=get_param(params, 'sendingChemicalName')
            )
        except Exception:
            sending_chem = None
        if sending_chem:
            requirements.append(f'(chemical.id == {sending_chem.id})')
        # print(sending_chem)

        try:
            chem_cat = get_param(params, 'chemicalCategory')
            if chem_cat and (chem_cat.upper().strip() != 'ALL'):
                requirements.append(f'chemical.isa("{chem_cat}")')
        except Exception:
            pass

        require_comps = [
            ('sendingCompartmentCategory', 'sender'),
            ('receivingCompartmentCategory', 'receiver')
        ]
        for param, name in require_comps:
            m_name = get_param(params, param)
            if m_name.upper().strip() == 'ALL':
                continue

            if m_name.lower().startswith('pseudosource'):
                orig_m_name = m_name.lower()
                m_name = 'Source'
                if 'vapor' in orig_m_name:
                    m_name = 'VaporSource'
                elif 'particle' in orig_m_name:
                    m_name = 'ParticleSource'
                if 'wet' in orig_m_name:
                    m_name = f'Wet{m_name}'
                elif 'dry' in orig_m_name:
                    m_name = f'Dry{m_name}'
            elif 'Sink' in m_name:
                m_name = m_name.lower()
                if 'degradation' in m_name:
                    m_name = 'Degradation_Reaction_Sink'
                elif 'soil_advection' in m_name:
                    m_name = 'Soil_Advection_Sink'
                elif 'soil' in m_name:
                    m_name = 'Soil_Sink'
                elif 'air' in m_name:
                    m_name = 'Air_Advection_Sink'
                elif 'water' in m_name:
                    m_name = 'Flush_Rate_Sink'
                elif 'sediment' in m_name:
                    m_name = 'Sediment_Sink'
            else:
                m_name = m_name.split('|')[-1].strip()
                m_name = m_name.replace(' - Default', '')
                m_name = m_name.replace(' / ', '_').replace('/', '_')
                m_name = m_name.replace(' - ', '_').replace(' ', '_')

            m_name = MEDIA_MAP.get(m_name, m_name)

            if m_name in ['Leaf', 'Leaf_Particle', 'Stem', 'Root']:
                m_names = [
                    v for v in MEDIA_MAP.values() if v.endswith(f'_{m_name}')
                ]
            else:
                m_names = [m_name]

            # print(m_names)

            media = [
                CompartmentService.media.get(category=m) for m in m_names
            ]
            media = [m for m in media if m is not None]

            # print(media)
            if media:
                or_media = [
                    f'{name}.media.isa("{m.category}")' for m in media
                ]
                requirements.append(f'({" or ".join(or_media)})')

        comp_relationship = get_param(params, 'compartmentRelationship')
        if comp_relationship == 'ABOVE_OR_BELOW':
            requirements.append('sender.id != receiver.id')
            requirements.append(
                'sender.volume_element.parcel.id'
                ' == receiver.volume_element.parcel.id'
            )
        elif comp_relationship in [
            'IN_SAME_VOLUME_ELEMENT', 'IN_SAME_COMPOSITE'
        ]:
            requirements.append('sender.id != receiver.id')
            requirements.append(
                'sender.volume_element.id'
                ' == receiver.volume_element.id'
            )
        elif comp_relationship == 'NEXT_TO':
            requirements.append(
                'sender.is_next_to(receiver)'
            )
        elif comp_relationship == 'SENDER_ABOVE':
            requirements.append('sender.id != receiver.id')
            requirements.append(
                'sender.volume_element.parcel.id'
                ' == receiver.volume_element.parcel.id'
            )
            requirements.append(
                'sender.volume_element.bottom >'
                ' receiver.volume_element.bottom'
            )
        elif comp_relationship == 'SENDER_BELOW':
            requirements.append('sender.id != receiver.id')
            requirements.append(
                'sender.volume_element.parcel.id'
                ' == receiver.volume_element.parcel.id'
            )
            requirements.append(
                'sender.volume_element.top <'
                ' receiver.volume_element.top'
            )
        elif comp_relationship == 'SAME':
            requirements.append(
                'sender.id == receiver.id'
            )

        # print(requirements)
        if requirements:
            proc.requirements = ' and '.join(requirements)

        TransportProcessService.commit()
