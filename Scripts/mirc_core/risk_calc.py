from .equations import *
from .utils import log_vals
from trim_db.schema import MircLifeStage as LifeStage


__all__ = ['assess_risk']


def assess_risk(
    scenario, product, chemical,
    concentration=None, concentration_fat=None, concentration_aq=None,
    ingestion_percentile='Pmean', body_weight_percentile='Pmean',
    logs=[]
):
    if (
        concentration is None
        and concentration_fat is None
        and concentration_aq is None
    ):
        logs.append(f"No concentrations > 0 for {product} in this scenario; moving on ...")
        return None

    chem_params = scenario.parameters.for_chemical(chemical)
    product_params = scenario.parameters.for_media(product)

    loss_factors = product_params.LF

    logs.append(
        "In this scenario, loss factors "
        f"for {product} = {loss_factors}"
    )

    ureg = scenario.parameters.unit_registry  # Get active unit registry

    FC = product_params.FC.value or 1
    EF = product_params.EF.quantity or (350 * ureg('day'))

    logs.append(f'\nGot parameters for {product} from scenario:')
    log_vals(logs, FC=FC, EF=EF)

    adj_factor = None
    if product.is_a('fish'):
        # Get params by-chemical by-animal for product
        chem_animal_params = chem_params.for_media(product)
        adj_factor = chem_animal_params.FishAdjFactor.value
    elif product.name == 'soil':
        adj_factor = chem_params.SoilAdjFactor.value

    adj_factor = adj_factor or 1
    logs.append(
        "\nGot a cooking adjustment factor of "
        f"{adj_factor} for {product} for {chemical} in scenario"
    )

    pct_params = scenario.parameters.for_food(
        product
    ).at_percentile(ingestion_percentile)

    base_intake = {}
    adafs = {}

    irs = pct_params.IR

    for ir_param in irs:
        if ir_param.media is not None:
            continue

        age = ir_param.life_stage

        if not ir_param:
            if product.name == 'water':
                IR = 0 * ureg('mL/day')
            else:
                IR = 0 * ureg('g/day/kg')
        else:
            IR = ir_param.quantity

        logs.append(f"\nGot IR = {IR} for {product} for {age} in scenario")

        if product.name == 'breast milk':
            if IR == 0:
                IR = 0 * ureg('kg/day')
            f_mbm = product_params.f_mbm.value
            AE_inf = chem_params.for_media(product).AE_inf.value
            BW_inf = scenario.parameters.at_percentile(
                body_weight_percentile
            ).at_life_stage(age).BW.quantity
            logs.append(f"Got BW_inf = {BW_inf} for {age} in scenario")

            # We need to round this to make it match our old results,
            # which always used a rounded infant bw instead of the
            # unrounded version stored in the main bw table
            BW_inf = round(BW_inf, 1)
            logs.append(f"Rounded BW_inf = {BW_inf}")

            intake = get_average_daily_dose_to_nursing_infant(
                concentration_fat, f_mbm, concentration_aq,
                IR, AE_inf, EF, BW_inf
            )
        else:
            if IR == 0:
                IR = 0 * ureg('g/day/kg')
            # Check if the ingestion rate needs to be body-weight adjusted
            if not IR.check('[mass]/[time]/[mass]'):
                body_weight = scenario.parameters.at_percentile(
                    body_weight_percentile
                ).at_life_stage(age).BW.quantity
                logs.append(
                    f"Got body_weight = {body_weight} for {age} in scenario"
                )
                if body_weight == 0:
                    raise ValueError(
                        f'Invalid Parameter: {body_weight_percentile.name} Body Weight'
                        f' for "{age.name}" = 0'
                        f' in Exposure Profile "{scenario.name}"'
                    )

                IR = IR / body_weight
                logs.append(f"Adjusted IR = {IR}")

            intake = concentration * IR
            intake = intake * adj_factor
            intake = intake * FC * (EF / (365 * ureg('day')))

            for lf in loss_factors:
                intake = intake * (1 - lf.value)

        intake = intake.to('mg/day/kg')

        logs.append(
            f"Calculated {chemical} intake from {product} "
            f"for {age}: {intake}"
        )
        base_intake[age.name] = intake

        adaf = chem_params.at_life_stage(age).ADAF.quantity
        adafs[age.name] = adaf

    ages = {
        ls.name: ls.duration * ureg(ls.duration_unit)
        for ls in LifeStage.query.all()
        if ls.name != 'Pregnant Mother'
    }
    lifespan = max(70 * ureg('year'), sum(ages.values()))

    RfD = chem_params.RfD.quantity
    logs.append(f"\nGot RfD = {RfD} for {chemical} in scenario")

    CSF = chem_params.CSF.quantity
    logs.append(f"\nGot CSF = {CSF} for {chemical} in scenario")

    risk_data = {}

    LADD = 0
    LADD_adj = None
    for age, span in ages.items():
        val = base_intake.get(age, 0 * ureg('mg/day/kg'))
        LADD += val * span / lifespan

        adj = None
        adaf = adafs.get(age)
        if adaf:
            logs.append(
                "\nIn this scenario, mutagenic adjustment factor "
                f"for {chemical} at {age} = {adaf}"
            )
            adj = val * adaf
            logs.append(
                f"Calculated adjusted {chemical} intake from {product} "
                f"for {age}: {adj}"
            )
            if LADD_adj is None:
                LADD_adj = 0
            LADD_adj += adj * span / lifespan

        hq = None
        if RfD:
            i = adj if adj is not None else val
            hq = i / RfD

        # elcr = None  # We are not reporting risk_factor for individual life stages
        if CSF:
            i = adj if adj is not None else val
            # elcr = i * CSF

        risk_data[age] = {
            'intake': val,
            'adjusted_intake': adj,
            'hazard_quotient': hq,
            'risk_factor': 'N/A'  # elcr
        }

    logs.append(
        f"\nCalculated {chemical} intake from {product} "
        f"for LADD: {LADD}"
    )

    if LADD_adj:
        logs.append(
            f"\nCalculated adjusted {chemical} intake from {product} "
            f"for LADD: {LADD_adj}"
        )

    LADD_hq = None
    if RfD:
        i = LADD_adj if LADD_adj is not None else LADD
        LADD_hq = i / RfD

    LADD_elcr = None
    if CSF:
        i = LADD_adj if LADD_adj is not None else LADD
        LADD_elcr = i * CSF

    risk_data['Lifetime'] = {
        'intake': LADD,
        'adjusted_intake': LADD_adj,
        'hazard_quotient': LADD_hq,
        'risk_factor': LADD_elcr
    }

    return risk_data
