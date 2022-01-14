from ..services import TransportProcessService, FormulaService, \
    ChemicalService, CompartmentService
from ..schema.parameters.equations import deconstruct_equation
from .environment import MEDIA_MAP

__all__ = ['parse_transport_processes']


TRANSFER_ALGORITHMS = [
    'Degradation/Reaction Sink in Sediment(AlgInstID_4565)',
    'Degradation/Reaction Sink in Surface Water(AlgInstID_4585)',
    'Demethylation(MHg -> Hg2) in Abiotic Media, Rate is input(AlgInstID_1892)',  # noqa
    'Diffusion from Sediment to Surface Water, Fugacity-based(AlgInstID_2195)',
    'Diffusion from Surface Water to Sediment, Fugacity-based(AlgInstID_2149)',
    'Methylation(Hg2 -> MHg) in Abiotic Media, Rate is input(AlgInstID_1891)',
    'Oxidation(Hg0 -> Hg2) in Abiotic Media, Rate is input(AlgInstID_1894)',
    'Reduction(Hg2 -> Hg0) in Abiotic Media, Rate is input(AlgInstID_1893)',
    'Resuspension from Sediment to Surface Water, General(AlgInstID_2190)',
    'Sediment Burial from Sediment to Sediment Burial Sink, Zero net deposition, General(AlgInstID_4135)',  # noqa
    'Sediment Deposition from Surface Water to Sediment, General(AlgInstID_2139)',  # noqa

    'Fish Bioenergetic Model - Ingestion of Algae by Fish(AlgInstID_1527)',
    'Fish Bioenergetic Model - Ingestion of Algae by Zooplankton',
    'Fish Bioenergetic Model - Ingestion of Benthic Carnivore by Benthic Omnivore(AlgInstID_1455)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Benthic Carnivore by Water Column Carnivore(AlgInstID_2245)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Benthic Carnivore by Water Column Omnivore(AlgInstID_2277)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Benthic Invertebrate by Benthic Carnivore(ICFID_08-001)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Benthic Invertebrate by Benthic Omnivore(AlgInstID_1467)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Benthic Invertebrate by Water Column Carnivore(AlgInstID_2255)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Benthic Invertebrate by Water Column Herbivore(AlgInstID_2270)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Benthic Invertebrate by Water Column Omnivore(AlgInstID_2287)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Benthic Omnivore by Benthic Carnivore(AlgInstID_1447)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Benthic Omnivore by Water Column Carnivore(AlgInstID_2250)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Benthic Omnivore by Water Column Omnivore(AlgInstID_2282)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Macrophyte by Water Column Herbivore(AlgInstID_1646)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Macrophyte by Water Column Omnivore(AlgInstID_1655)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Water Column Carnivore by Benthic Carnivore(AlgInstID_2158)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Water Column Carnivore by Benthic Omnivore(AlgInstID_2175)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Water Column Carnivore by Water Column Omnivore(AlgInstID_1618)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Water Column Herbivore by Benthic Carnivore(AlgInstID_2163)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Water Column Herbivore by Benthic Omnivore(AlgInstID_2180)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Water Column Herbivore by Water Column Carnivore(AlgInstID_1600)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Water Column Herbivore by Water Column Omnivore(AlgInstID_1638)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Water Column Omnivore by Benthic Carnivore(AlgInstID_2168)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Water Column Omnivore by Benthic Omnivore(AlgInstID_2185)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Water Column Omnivore by Water Column Carnivore(AlgInstID_1610)',  # noqa
    'Fish Bioenergetic Model - Ingestion of Zooplankton by Water Column Herbivore',  # noqa

    'Exchange from Macrophyte to Surface Water(AlgInstID_1547)',
    'Degradation/Reaction Sink in Macrophyte',
    # 'Oxidation(Hg0 -> Hg2) in Macrophytes',  # Covered by Fish
    'Time-dependent Partition from Surface Water to Macrophyte, Hg(AlgInstID_1549)',  # noqa
    'Time-dependent Partition from Macrophyte to Surface Water(AlgInstID_1544),Hg',  # noqa

    'Time-dependent Partition from Sediment to Benthic Invertebrate(AlgInstID_1438)',  # noqa
    'Time-dependent Partition from Benthic Invertebrate to Sediment(AlgInstID_1433)',  # noqa

    'Degradation/Reaction Sink in Zooplankton(AlgInstID_4570_Z)',
    # 'Elimination from Zooplankton to Surface Water',  # Covered by Fish
    'Elimination from Fish to Surface Water(AlgInstID_1512)',

    'Demethylation (MHg->Hg2) in Fish(AlgInstID_1446)',
    'Oxidation(Hg0 -> Hg2) in Fish(AlgInstID_1443)',
    'Reduction(Hg2 -> Hg0) in Fish(AlgInstID_1444)',

    'Bulk Advection from Surface Water to Flush-rate Advection Sink, General(AlgInstID_4125)',  # noqa
    'Diffusion from Surface Water to Air, Two Film(AlgInstID_4080)-Hg',
    'Algae Deposition from Surface Water to Sediment, General(AlgInstID_2144)',

    'Waterflow from Surface Water to Surface Water, General(AlgInstID_3685)',

    'Direct Transfer from PseudoSource to Surface water'
]


def parse_transport_processes(algorithm_parameters):
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
        if name not in TRANSFER_ALGORITHMS:
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

        require_comps = [
            ('sendingCompartmentCategory', 'sender'),
            ('receivingCompartmentCategory', 'receiver')
        ]
        for param, name in require_comps:
            m_name = get_param(params, param)

            if m_name.lower() == 'pseudosource':
                m_name = 'Source'
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

        # print(requirements)
        if requirements:
            proc.requirements = ' and '.join(requirements)

        TransportProcessService.commit()
