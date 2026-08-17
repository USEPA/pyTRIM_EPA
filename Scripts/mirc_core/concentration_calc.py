from .equations import *
from .utils import log_vals, output_units

__all__ = ['calculate_c_product']


def calculate_c_product(
    scenario, product, chemical, simulation,
    logs=[], **kwargs
):
    if product.name == 'soil':
        return calculate_c_soil(
            chemical, scenario, simulation, logs=logs
        )

    elif product.name == 'water':
        return calculate_c_water(
            chemical, scenario, simulation, logs=logs
        )

    elif product.name == 'breast milk':
        return calculate_c_breast_milk(
            scenario, product, chemical,
            kwargs.get('maternal_cumulative_ladd'),
            logs=logs
        )

    elif product.is_a('livestock'):
        return calculate_c_animal(
            product, chemical, scenario, simulation, logs=logs
        )

    elif product.is_a('plant'):
        return calculate_c_plant(
            product, chemical, scenario, simulation, logs=logs
        )

    elif product.is_a('fish'):
        return calculate_c_fish(
            chemical, scenario, simulation, logs=logs
        )

    raise NotImplementedError


@output_units('mg/kg')
def calculate_c_animal(
    product, chemical, scenario, simulation,
    logs=[]
):
    if not product.is_a('animal'):
        raise TypeError

    # Extract input vals
    # Bs = simulation.get_parameter('Bs').quantity
    chem_params = scenario.parameters.for_chemical(chemical)
    animal_params = scenario.parameters.for_media(product)

    # Fraction of wet deposition that adheres to plant surfaces
    Fw = chem_params.Fw.value

    # Get params by-chemical by-animal for product
    chem_animal_params = chem_params.for_media(product)

    Bs = chem_animal_params.Bs
    Bs = Bs.value if Bs else 1

    # Chemical-specific biotransfer factor for chemical
    Ba = chem_animal_params.Ba.quantity

    # Chemical-specific mammalian metabolism factor
    MF = chem_animal_params.MF
    MF = MF.value if MF else 1

    # Chemical concentration in surface soil
    # Cs_s = chem_animal_params.Bs
    Cs_s = simulation.get_parameter('Cs_s').quantity

    logs.append('Got variables from scenario:')
    log_vals(
        logs,
        Fw=Fw,
        Ba=Ba, MF=MF, Cs_s=Cs_s
    )

    logs.append("\nCalculating chemical intakes from feed")

    plant_ch_intakes = []  # list of all plant-chemical intakes
    for feed_ir in animal_params.IR:
        feed = feed_ir.food
        if feed.name == 'soil':
            # Quantity of soil eaten by livestock each day
            Qs = feed_ir.quantity

            logs.append(f"Got Qs = {Qs} for {feed} in scenario")

            # Incidental ingestion of chemical in surface soils by livestock
            soil_ch_intake = get_soil_ch_intake(Qs=Qs, Cs_s=Cs_s, Bs=Bs)
            logs.append(
                f"\nCalculated chemical intake from soil: {soil_ch_intake}"
            )

        else:
            C_feed = calculate_c_plant(
                feed, chemical, scenario, simulation, dry_weight=True
            )
            logs.append(f"Calculated C_feed for {feed}: {C_feed}")

            # Quantity of plant feed type i consumed per animal per day
            Qp = feed_ir.quantity
            logs.append(f"Got Qp = {Qp} for {feed} in scenario")

            # Fraction of plant feed type i obtained from contaminated area
            F = scenario.parameters.for_media(feed).FC.value
            logs.append(f"Got F = {F} for {feed} in scenario")

            # Concentration of chemical in ingested plant feed type i
            ch_intake = get_plant_ch_intake(F=F, Qp=Qp, C=C_feed)
            logs.append(f"Calculated ch_intake for {feed}: {ch_intake}\n")

            plant_ch_intakes.append(ch_intake)  # add to list

    # Concentration of chemical in product

    if product.is_a('poultry'):
        # No real need to have a separate function for this,
        # but we'll do it this way for now because this
        # is how it was done in RTR TSD Appendix B
        c_product = get_c_poultry(
            Ba=Ba,
            Soil_Ch_Intake=soil_ch_intake,
            Plant_Ch_Intakes=plant_ch_intakes[0]  # I.e., only grain
        )
    else:
        c_product = get_c_mammal(
            Ba=Ba, MF=MF,
            Soil_Ch_Intake=soil_ch_intake,
            Plant_Ch_Intakes=plant_ch_intakes
        )

    return c_product


@output_units('mg/kg')
def calculate_c_plant(
    product, chemical, scenario, simulation, dry_weight=False,
    logs=[]
):
    if not product.is_a('plant'):
        raise TypeError

    if product.name == 'root':
        return calculate_c_root(
            product, chemical, scenario, simulation,
            dry_weight=False
        )

    # Extract input vals
    if product.is_feed:
        logs.append('Using feed Cs ...')
        Cs_root_zone = simulation.get_parameter('Cs_root_zone').quantity
    else:
        logs.append('Using garden Cs ...')
        Cs_root_zone = simulation.get_parameter('C_root_veg').quantity
    Ca = simulation.get_parameter('Ca').quantity
    Drdp = simulation.get_parameter('Drdp').quantity
    Drwp = simulation.get_parameter('Drwp').quantity
    Fv = simulation.get_parameter('Fv').quantity
    rho_a = simulation.get_parameter('rho_a').quantity

    chem_params = scenario.parameters.for_chemical(chemical)
    plant_params = scenario.parameters.for_media(product)

    # Get params by-chemical by-plant
    chem_plant_params = chem_params.for_media(product)

    # Chemical-specific plant-soil bioconcentration factor
    Br = chem_plant_params.Br.value
    logs.append(f"\nGot Br = {Br} for {product} in scenario")

    # Concentration of chemical in plant due to root uptake
    Pr_produce = get_pr_ag_produce_dw(Cs_root_zone=Cs_root_zone, Br=Br)
    logs.append(f"Calculated Pr for {product}: {Pr_produce}")

    if product.is_a('protected plant'):
        # Pd and Pv don't apply to protected plant products
        # because they are protected from air by husks/pods
        Pd = 0
        Pv = 0
    else:
        # Fraction of wet deposition that adheres to plant surfaces
        Fw = chem_params.Fw.value

        logs.append('Got variables from scenario:')
        log_vals(
            logs,
            Fw=Fw
        )

        # Interception fraction of the edible portion of plant
        Rp = plant_params.Rp.value

        # Plant surface loss coefficient for plant
        kp = plant_params.kp.quantity

        # Length of exposure to deposition in the field per harvest
        # of the edible portion of plant
        Tp = plant_params.Tp.quantity

        # Yield or standing crop biomass of the edible portion
        # of plant
        Yp = plant_params.Yp.quantity

        logs.append(f'Got parameters for {product} from scenario:')
        log_vals(
            logs, Rp=Rp, kp=kp, Tp=Tp, Yp=Yp)

        # Chemical concentration in aboveground produce
        # due to particle deposition
        Pd = get_pd(
            Drdp=Drdp, Drwp=Drwp, Fw=Fw,
            Rp=Rp, kp=kp, Tp=Tp, Yp=Yp
        )
        logs.append(f"Calculated Pd for {product}: {Pd}")

        # Empirical correction factor for aboveground
        # exposed produce
        VG_AG = chem_plant_params.VG.value
        logs.append(f"Got VG_AG = {VG_AG} for {product} in scenario")

        # Air-to-plant biotransfer factor for aboveground produce
        # for vapor-phase chemical
        Bv_AG = chem_plant_params.Bv_ag.value
        logs.append(f"Got Bv_ag = {Bv_AG} for {product} in scenario")

        # Concentration of chemical in aboveground produce
        # from air-to-plant transfer of vapor-phase chemical
        Pv = get_pv(
            Ca=Ca, Fv=Fv, Bv_AG=Bv_AG, VG_AG=VG_AG, rho_a=rho_a
        )
        logs.append(f"Calculated Pv for {product}: {Pv}")

    # Concentration of chemical in plant
    C_produce_dw = get_c_ag_produce_dw(Pr=Pr_produce, Pd=Pd, Pv=Pv)
    logs.append(f"Calculated C_produce_dw for {product}: {C_produce_dw}")

    if dry_weight:
        c_product = C_produce_dw
    else:
        # Moisture adjustment factor
        MAF = plant_params.MAF.value * 100
        logs.append(f"Got MAF = {MAF} in scenario")

        c_product = convert_c_ag_produce_ww(C_produce_dw, MAF)

    return c_product


@output_units('mg/kg')
def calculate_c_root(
    product, chemical, scenario, simulation, dry_weight=False,
    logs=[]
):
    if product.name != 'root':
        raise TypeError

    # Extract input vals
    if product.is_feed:
        logs.append('Using feed Cs ...')
        Cs_root_zone = simulation.get_parameter('Cs_root_zone').quantity
    else:
        logs.append('Using garden Cs ...')
        Cs_root_zone = simulation.get_parameter('C_root_veg').quantity

    chem_params = scenario.parameters.for_chemical(chemical)
    plant_params = scenario.parameters.for_media(product)

    # Get params by-chemical by-plant
    chem_plant_params = chem_params.for_media(product)

    # Chemical-specific plant-soil bioconcentration factor
    Br = chem_plant_params.Br.value
    logs.append(f"\nGot Br = {Br} for {product} in scenario")

    VG_rootveg = chem_plant_params.VG.value
    logs.append(f"\nGot VG_rootveg = {VG_rootveg} for {product} in scenario")

    if chemical.inorganic:
        logs.append(f'{chemical} is inorganic')

        # Concentration of chemical in plant
        C_produce_dw = get_c_bg_produce_dw_br(
            Cs_root_zone=Cs_root_zone, Br=Br, VG=VG_rootveg
        )
        logs.append(f"Calculated C_produce_dw for {product}: {C_produce_dw}")
    else:
        logs.append(f'{chemical} is organic')

        RCF = chem_plant_params.RCF.quantity
        logs.append(f"\nGot RCF = {RCF} for {product} in scenario")

        if product.is_feed:
            Kds = simulation.get_parameter('Kds_feed')
            if not Kds:
                Kds = chem_params.Kds
            Kds = Kds.quantity
        else:
            Kds = simulation.get_parameter('Kds')
            if not Kds:
                Kds = chem_params.Kds
            Kds = Kds.quantity

        # Concentration of chemical in plant
        C_produce_dw = get_c_bg_produce_dw_rcf(
            Cs_root_zone=Cs_root_zone, RCF=RCF, VG=VG_rootveg, Kds=Kds
        )
        logs.append(f"Calculated C_produce_dw for {product}: {C_produce_dw}")

    if dry_weight:
        c_product = C_produce_dw
    else:
        # Moisture adjustment factor
        MAF = plant_params.MAF.value * 100
        logs.append(f"Got MAF = {MAF} in scenario")

        c_product = convert_c_bg_produce_ww(C_produce_dw, MAF)

    return c_product


@output_units('mg/kg')
def calculate_c_fish(chemical, scenario, simulation, logs=[]):
    ureg = scenario.parameters.unit_registry  # Get active unit registry
    if simulation.use_baf:
        logs.append(f"Factor Type: BAF/BSAF")

        chem_params = scenario.parameters.for_chemical(chemical)

        C_surf_water = simulation.get_parameter('C_surf_water').quantity
        C_sed = simulation.get_parameter('C_sed').quantity
        FMD = simulation.get_parameter('FMD').quantity

        logs.append(f'Got parameters for fish:')
        log_vals(
            logs,
            C_sed=C_sed,
            C_surf_water=C_surf_water,
            FMD=FMD
        )

        C_total_fish = 0 * ureg('mg/kg')
        for consumption in simulation.consumption_breakdowns:
            fish_type = consumption.subfood
            if not fish_type.is_a('fish') or fish_type.name == 'fish':
                continue

            f_fish = consumption.fraction

            logs.append(
                f'Got f_{fish_type.name.replace(" ", "_")} = {f_fish}:'
            )

            baf = chem_params.for_media(fish_type).BAF
            if not baf:
                baf = chem_params.for_media(fish_type).BSAF
            if not baf:
                raise TypeError(
                    'There is no BAF/BSAF parameter defined'
                    f' for {chemical.hap_name}, {fish_type}'
                )

            logs.append(f'Got B(S)AF for {fish_type.name} = {baf.quantity}')

            C_src = (
                C_sed if baf.variable == 'BSAF'
                else C_surf_water * FMD
            )

            C_total_fish += (baf.quantity * C_src * f_fish)

    else:
        logs.append(f"Factor Type: Normal")

        C_total_fish = 0 * ureg('mg/kg')
        for consumption in simulation.consumption_breakdowns:
            fish_type = consumption.subfood
            if not fish_type.is_a('fish') or fish_type.name == 'fish':
                continue

            f_fish = consumption.fraction

            logs.append(
                f'Got f_{fish_type.name.replace(" ", "_")} = {f_fish}:'
            )

            c_fish = simulation.get_parameter(
                'C_' + fish_type.name.replace(' ', '_')
            )
            if not c_fish:
                continue
            c_fish = c_fish.quantity

            logs.append(
                f'Got c_{fish_type.name.replace(" ", "_")} = {c_fish}:'
            )

            C_total_fish += (c_fish * f_fish)

    c_product = C_total_fish

    return c_product


@output_units('mg/kg')
def calculate_c_soil(chemical, scenario, simulation, logs=[]):
    # Get soil concentration from TRIM input
    c_product = simulation.get_parameter('C_soil').quantity

    return c_product


@output_units('g/L')
def calculate_c_water(chemical, scenario, simulation, logs=[]):
    # Get drinking water concentration from TRIM input
    c_product = simulation.get_parameter('C_water')
    if c_product:
        c_product = c_product.quantity
    else:
        ureg = scenario.parameters.unit_registry  # Get active unit registry
        c_product = 0 * ureg('g/L')

    return c_product


@output_units('mg/kg', 'mg/kg')
def calculate_c_breast_milk(
    scenario, product, chemical, maternal_cumulative_ladd,
    logs=[]
):
    chem_params = scenario.parameters.for_chemical(chemical)
    product_params = scenario.parameters.for_media(product)
    chem_bm_params = chem_params.for_media(product)

    if not chem_bm_params.AE_inf.value:
        return None, None

    BM_pct = 'P90'

    pct_params = scenario.parameters.for_food(
        product
    ).at_percentile(BM_pct)

    ir_param = pct_params.IR
    for ir in ir_param:
        if '<1' in ir.life_stage.name:
            ir_param = ir
            break
    IR = ir_param.quantity

    # infancy absorption efficiency (1)
    aeinf = chem_bm_params.AE_inf.value

    # maternal absorption efficiency (1)
    aemat = chem_bm_params.AE_mat.value

    # fraction in maternal body fat  (1)
    ff = chem_bm_params.f_f.value

    # half life  (1)
    h = chem_bm_params.h_bm.quantity

    # nonlactating elimination rate constant  (1)
    kelim = chem_bm_params.k_elim.quantity

    # fraction breast milk fat
    fmbm = product_params.f_mbm.value

    # fraction maternal weight fat
    ffm = product_params.f_fm.value

    # maternal exposure duration
    tpn = product_params.t_pn.quantity

    # fraction maternal weight plasma
    fpm = product_params.f_pm.value

    # Mean infant milk ingestion rate over duration of nursing (kg/day)
    IRmilk = IR

    # Partition coefficient for chemical
    # between the plasma and breast milk in the aqueous phase (unitless);
    # assumed to equal 1.0
    pcbm = chem_bm_params.PC_pl_aq.quantity

    # Partition coefficient for chemical
    # between red blood cells and plasma (unitless);
    # chemical-specific
    pcrbc = chem_bm_params.PC_rbc_pl.quantity

    # Fraction of steady-state total body burden
    # of hydrophilic chemical in mother
    # that is in the mother’s whole blood compartment (unitless)
    fbl = chem_bm_params.f_bl.value

    # Fraction of mother’s whole blood that is plasma
    fbp = chem_bm_params.f_pl.value

    logs.append('Got variables from scenario:')
    log_vals(
        logs,
        AE_inf=aeinf, AE_mat=aemat,
        f_f=ff, h=h,
        k_elim=kelim,
        f_mbm=fmbm, f_fm=ffm,
        tpn=tpn, f_pm=fpm,
        IR_milk=IRmilk,
        Pc_bm=pcbm, Pc_RBC=pcrbc,
        f_bl=fbl, f_bp=fbp
    )

    # Body weight of mother (kg) averaged over duration of mother’s exposure
    BW_mat = scenario.parameters.at_percentile('Pmean').at_life_stage(
        'Pregnant Mother'
    ).BW.quantity
    logs.append(f"Got BW_mat = {BW_mat} in scenario")

    # Body weight of infant (kg) averaged over duration of nursing exposure
    BW_inf = scenario.parameters.at_percentile('Pmean').at_life_stage(
        'Child <1'
    ).BW.quantity
    logs.append(f"Got BW_inf = {BW_inf} in scenario")

    # Duration of breast feeding (days)
    tbf = product_params.EF.quantity
    logs.append(f"Got tbf = {tbf} in scenario")

    maternal_add = maternal_cumulative_ladd
    logs.append(f"\nGot ADD_mat = {maternal_add}")

    # kelim = np.log(2) / h NOT NEEDED ALWAYS 0.00019 regardless of chemical
    DAI = get_maternal_intake(maternal_add, aemat)
    logs.append(f"\nCalculated DAI_mat = {DAI}")

    kfat_elac = get_biolgical_elimination_rate_lactating(
        kelim, IRmilk, ff, fmbm, ffm, BW_mat
    )
    logs.append(f"\nCalculated k_fat_elac = {kfat_elac}")

    c_fat = get_pr_breastmilk_fat(DAI, ff, kelim, ffm, kfat_elac, tbf, tpn)

    try:
        fpl = get_fraction_blood_plasma(fbl, fbp, pcrbc)
        logs.append(f"\nCalculated f_pl = {fpl}")

        DAI_mat = get_maternal_intake(maternal_add, aemat)
        logs.append(f"\nUpdated DAI_mat = {DAI_mat}")

        kaq_elac = get_biolgical_elimination_rate_lactating(
            kelim, IRmilk, ff, fmbm, ffm, BW_mat
        )
        logs.append(f"\nCalculated k_aq_elac = {kaq_elac}")

        c_aqueous = get_pr_aqueous_breastmilk(
            DAI_mat, fpl, pcbm, kaq_elac, fpm
        )
    except ZeroDivisionError:
        c_aqueous = 0

    logs.append(f"\nCalculated c_aqueous = {c_aqueous}")
    logs.append(f"\nCalculated c_fat = {c_fat}")

    ADD_BM = get_average_daily_dose_to_nursing_infant(
        c_fat, fmbm, c_aqueous, IRmilk, aeinf, tbf, BW_inf
    )

    logs.append(f"\nCalculated ADD_bm = {ADD_BM}")

    return (c_fat, c_aqueous)
