import pandas as pd
from trim_db.services import ChemicalService, \
    MircProductService, MircLifeStageService, MircPercentileService


# ===========================================
# Model helpers
# ===========================================


def get_chemicals(chemical_id=None):
    if chemical_id is None:
        chems = ChemicalService.get_all()
    else:
        chems = [ChemicalService.get(chemical_id)]
    return list(sorted(chems, key=lambda x: x.name))


def get_products(product_id=None):
    if product_id is None:
        prods = MircProductService.get_all()
    else:
        prods = [MircProductService.get(product_id)]
    return list(sorted(prods, key=lambda x: x.name))


def get_ages(age_id=None):
    if age_id is None:
        ages = MircLifeStageService.get_all()
    else:
        ages = [MircLifeStageService.get(age_id)]
    return list(sorted(ages, key=lambda x: MircLifeStageService.as_orderable(x)))


def get_percentiles(percentile_id=None, include_no_percentile=False):
    if percentile_id is None:
        if include_no_percentile:
            MircPercentileService.get_all()
        else:
            pcts = [
                p for p in MircPercentileService.get_all()
                if p.name.lower() != 'none'
            ]
    else:
        pcts = [MircPercentileService.get(percentile_id)]

    return pcts


# ===========================================
# Data retrieval helpers
# ===========================================


def get_human_ingestion_rates(scenario, age_id=None, percentile_id=None, include_no_percentile=False):
    prods = get_products()
    ages = get_ages(age_id=age_id)
    pcts = get_percentiles(percentile_id=percentile_id, include_no_percentile=include_no_percentile)

    irs = []

    for p in prods:
        if not p.is_food:
            continue
        for age in ages:
            if age.name == 'Pregnant Mother':
                continue
            for pct in pcts:
                data = {
                    'life_stage_id': age.id,
                    'life_stage': age.name.title(),
                    'percentile_id': pct.id,
                    'percentile': pct.name.title(),
                    'product_id': p.id,
                    'product': p.name.title()
                }
                ir = scenario.parameters.for_food(
                    p
                ).at_life_stage(age).at_percentile(pct).IR
                if ir:
                    data.update({
                        'rate': ir.value,
                        'unit': ir.unit,
                        'notes': ir.notes
                    })
                fc = scenario.parameters.for_media(p).FC
                if fc:
                    data.update({
                        'fraction_contaminated': fc.value
                    })

                irs.append(data)

    return irs


def get_human_body_weights(scenario, age_id=None, include_no_percentile=False):
    ages = get_ages(age_id=age_id)
    pcts = get_percentiles(include_no_percentile=include_no_percentile)

    bws = []

    for age in ages:
        for pct in pcts:
            data = {
                'life_stage_id': age.id,
                'life_stage': age.name.title(),
                'percentile_id': pct.id,
                'percentile': pct.name.title()
            }
            bw = scenario.parameters.at_life_stage(age).at_percentile(pct).BW
            if bw:
                data.update({
                    'value': bw.value,
                    'unit': bw.unit,
                    'notes': bw.notes
                })
            bws.append(data)

    return bws


def get_human_food_parameters(scenario, product_id=None):
    prods = get_products(product_id=product_id)

    fps = []

    for p in prods:
        if not p.is_food:
            continue
        p_props = scenario.parameters.for_media(p)
        if not p_props:
            continue
        data = {
            'product_id': p.id,
            'product': p.name.title(),
            'EF': p_props.EF.value
        }
        fps.append(data)

    return fps


def get_plant_parameters(scenario, product_id=None):
    prods = get_products(product_id=product_id)

    pps = []

    for p in prods:
        if not p.is_a('plant') or not (p.is_food or p.is_feed):
            continue

        plant_props = scenario.parameters.for_media(p)

        data = {
            'product_id': p.id,
            'product': p.name.title(),
            'MAF': plant_props.MAF.value,
            'Rp': plant_props.Rp.value,
            'kp': plant_props.kp.value,
            'kp_unit': plant_props.kp.unit,
            'Tp': plant_props.Tp.value,
            'Tp_unit': plant_props.Tp.unit,
            'Yp': plant_props.Yp.value,
            'Yp_unit': plant_props.Yp.unit
        }
        pps.append(data)

    return pps


def get_animal_ingestion_rates(scenario, consumer_id=None, product_id=None):
    consumers = get_products(product_id=consumer_id)
    prods = get_products(product_id=product_id)

    irs = []

    for c in consumers:
        if not c.is_a('animal') or not c.is_a('livestock') or not c.is_food:
            continue

        p_props = scenario.parameters.for_media(c)

        for p in prods:
            if not p.is_feed:
                continue
            data = {
                'consumer_id': c.id,
                'consumer': c.name.title(),
                'product_id': p.id,
                'product': p.name.title()
            }

            ir = p_props.for_food(p).IR
            if ir:
                data.update({
                    'rate': ir.value,
                    'unit': ir.unit,
                    'notes': ir.notes
                })
            fc = scenario.parameters.for_media(p).FC
            if fc:
                data.update({
                    'fraction_contaminated': fc.value
                })
            irs.append(data)

    return irs


def get_breast_milk_parameters(scenario):
    p = MircProductService.get(name='breast milk')

    bm_props = scenario.parameters.for_media(p)
    if not bm_props:
        return None

    data = {
        'f_mbm': bm_props.f_mbm.value,
        'f_fm': bm_props.f_fm.value,
        'f_pm': bm_props.f_pm.value,
        't_pn': bm_props.t_pn.value,
        't_pn_unit': bm_props.t_pn.unit
    }

    return data


def get_loss_factors(scenario, product_id=None):
    prods = get_products(product_id=product_id)

    loss_factors = []

    for p in prods:
        if not p.is_food:
            continue
        p_props = scenario.parameters.for_media(p)
        lfs = p_props.LF
        if not isinstance(lfs, list):
            lfs = [lfs]

        for lf in lfs:
            if lf.value == 0:
                continue
            data = {
                'product_id': p.id,
                'product': p.name.title(),
                'fraction_lost': lf.value,
                'loss_description': lf.name,
                'source': lf.source
            }
            loss_factors.append(data)

    return loss_factors


def get_chemical_parameters(scenario, chemical_id=None):
    chems = get_chemicals(chemical_id=chemical_id)

    cps = []

    for c in chems:
        chem_props = scenario.parameters.for_chemical(c)
        if not chem_props:
            continue

        data = {
            'chemical_id': c.id,
            'chemical': (c.hap_name or c.name).title(),
            'Fw': chem_props.Fw.value,
            'soil_adjustment': chem_props.SoilAdjFactor.value,
            'CSF': chem_props.CSF.value,
            'CSF_unit': chem_props.CSF.unit,
            'RfD': chem_props.RfD.value,
            'RfD_unit': chem_props.RfD.unit
        }
        cps.append(data)

    return cps


def get_mutagenic_parameters(scenario, chemical_id=None):
    chems = get_chemicals(chemical_id=chemical_id)
    ages = get_ages()

    mafs = []

    for c in chems:
        if not c.mutagenic:
            continue

        chem_props = scenario.parameters.for_chemical(c)
        if not chem_props:
            continue

        for age in ages:
            if age.name == 'Pregnant Mother':
                continue

            data = {
                'chemical_id': c.id,
                'chemical': (c.hap_name or c.name).title(),
                'life_stage_id': age.id,
                'life_stage': age.name
            }
            adaf = chem_props.at_life_stage(age).ADAF
            if adaf:
                data.update({
                    'value': adaf.value,
                    'notes': adaf.notes
                })

            mafs.append(data)

    return mafs


def get_baf_parameters(scenario, chemical_id=None):
    chems = get_chemicals(chemical_id=chemical_id)
    ats = get_products()

    bafs = []

    for c in chems:
        chem_props = scenario.parameters.for_chemical(c)
        if not chem_props:
            continue

        for at in ats:
            if not at.is_a('fish') or at.name == 'fish':
                continue
            nm = at.name.lower()
            ft = 'BSAF' if 'benthic' in nm else 'BAF'
            data = {
                'chemical_id': c.id,
                'chemical': (c.hap_name or c.name).title(),
                'aquatic_type_id': at.id,
                'aquatic_type': f'{nm.title()} ({ft})',
            }
            baf = chem_props.for_media(at).get_by_variable(ft)
            if baf:
                data.update({
                    'value': baf.value,
                    'unit': baf.unit,
                    'notes': baf.notes
                })

            bafs.append(data)

    return bafs


def get_plant_chemical_parameters(scenario, chemical_id=None, product_id=None):
    chems = get_chemicals(chemical_id=chemical_id)
    prods = get_products(product_id=product_id)

    pcps = []

    for c in chems:
        chem_props = scenario.parameters.for_chemical(c)
        if not chem_props:
            continue

        for p in prods:
            if not (p.is_a('plant') and (p.is_food or p.is_feed)):
                continue

            data = {
                'chemical_id': c.id,
                'chemical': (c.hap_name or c.name).title(),
                'product_id': p.id,
                'product': p.name
            }
            cp_props = chem_props.for_media(p)
            data.update({
                'Br': cp_props.Br.value,
                'VG': cp_props.VG.value,
                'Bv_ag': cp_props.Bv_ag.value,
                'RCF': cp_props.RCF.value,
                'RCF_unit': cp_props.RCF.unit,
                'notes': cp_props.notes
            })

            pcps.append(data)

    return pcps


def get_animal_chemical_parameters(scenario, chemical_id=None, product_id=None):
    chems = get_chemicals(chemical_id=chemical_id)
    prods = get_products(product_id=product_id)

    acps = []

    for c in chems:
        chem_props = scenario.parameters.for_chemical(c)
        if not chem_props:
            continue

        for p in prods:
            if not (p.is_a('animal') and p.is_food):
                continue

            data = {
                'chemical_id': c.id,
                'chemical': (c.hap_name or c.name).title(),
                'product_id': p.id,
                'product': p.name
            }
            ca_props = chem_props.for_media(p)
            data.update({
                'Bs': ca_props.Bs.value,
                'MF': ca_props.MF.value,
                'cooking_adjustment': ca_props.FishAdjFactor.value,
                'Ba': ca_props.Ba.value,
                'Ba_unit': ca_props.Ba.unit,
                'notes': ca_props.notes
            })

            acps.append(data)

    return acps


def get_breast_milk_chemical_parameters(scenario, chemical_id=None):
    chems = get_chemicals(chemical_id=chemical_id)
    p = MircProductService.get(name='breast milk')

    bmcps = []

    for c in chems:
        chem_props = scenario.parameters.for_chemical(c)
        if not chem_props:
            continue

        data = {
            'chemical_id': c.id,
            'chemical': (c.hap_name or c.name).title(),
            'product_id': p.id,
            'product': p.name
        }
        bm_props = chem_props.for_media(p)
        data.update({
            'AE_inf': bm_props.AE_inf.value,
            'AE_mat': bm_props.AE_mat.value,
            'f_bl': bm_props.f_bl.value,
            'f_f': bm_props.f_f.value,
            'f_pl': bm_props.f_pl.value,
            'h_bm': bm_props.h_bm.value,
            'h_bm_unit': bm_props.h_bm.unit,
            'k_elim': bm_props.k_elim.value,
            'k_elim_unit': bm_props.k_elim.unit,
            'k_aq_elac': bm_props.k_aq_elac.value,
            'k_aq_elac_unit': bm_props.k_aq_elac.unit,
            'PC_pl_aq': bm_props.PC_pl_aq.value,
            'PC_pl_aq_unit': bm_props.PC_pl_aq.unit,
            'PC_rbc_pl': bm_props.PC_rbc_pl.value,
            'PC_rbc_pl_unit': bm_props.PC_rbc_pl.unit,
            'notes': bm_props.notes
        })

        bmcps.append(data)

    return bmcps


# ===========================================
# Report Generation
# ===========================================


def multi_melt(df: pd.DataFrame, id_vars: list, value_vars: list):
    dfs = {}
    for i, _ in enumerate(value_vars[0]):
        n = i + 1

        n_df = df.melt(
            id_vars=id_vars,
            value_vars=[value_set[i] for value_set in value_vars if value_set[i] is not None],
            var_name=f'variable_{n}',
            value_name=f'value_{n}'
        )

        if i > 0:
            for j in range(i):
                jn = j + 1

                n_df[f'variable_{jn}'] = pd.NA

                for value_set in value_vars:
                    n_df.loc[
                        n_df[f'variable_{n}'] == value_set[i], f'variable_{jn}'
                    ] = value_set[j]

        dfs[i] = n_df

    # for i, df in dfs.items():
    #     print(f'============= {i} =============')
    #     print(df)

    base_df = dfs[0]
    for i in range(1, max(*list(dfs)) + 1):
        n_df = dfs[i]
        base_df = pd.merge(base_df, n_df, how='left')

    # print(base_df)

    return base_df


def make_report(scenario):
    def make_ir_report():
        irs = pd.DataFrame(
            get_human_ingestion_rates(scenario)
        ).drop(
            columns=['life_stage_id', 'percentile_id', 'product_id']
        )[[  # reorder
            'life_stage',
            'percentile',
            'product',
            'rate',
            'unit',
            'fraction_contaminated',
            'notes'
        ]].rename(columns={
            'life_stage': 'Life Stage',
            'percentile': 'Percentile',
            'product': 'Food Product',
            'fraction_contaminated': 'Fraction Contaminated',
            'rate': 'Ingestion Rate (IR)',
            'unit': 'IR Unit',
            'notes': 'Notes'
        })
        return irs

    def make_bw_report():
        bws = pd.DataFrame(
            get_human_body_weights(scenario)
        ).drop(
            columns=['life_stage_id', 'percentile_id']
        ).rename(columns={
            'life_stage': 'Life Stage',
            'percentile': 'Percentile',
            'value': 'Value',
            'unit': 'Unit',
            'notes': 'Notes'
        })
        return bws

    def make_hfp_report():
        hfps = pd.DataFrame(
            get_human_food_parameters(scenario)
        ).drop(
            columns=['product_id']
        ).melt(
            id_vars=['product'],
            value_vars=['EF']
        ).rename(columns={
            'product': 'Product',
            'variable': 'Parameter Name',
            'value': 'Value'
        })
        # add cols
        hfps['Parameter Name'] = 'Exposure Frequency'
        hfps['Unit'] = 'day'
        return hfps

    def make_pp_report():
        pps = pd.DataFrame(
            get_plant_parameters(scenario)
        ).drop(
            columns=['product_id']
        ).rename(columns={
            'MAF': 'Moisture Adjustment Factor',
            'Rp': 'Interception Fraction',
            'kp': 'Surface Loss Coefficient',
            'Tp': 'Exposure Length',
            'Yp': 'Standing Biomass'
        })
        pps = multi_melt(
            pps,
            id_vars=['product'],
            value_vars=[
                ('Moisture Adjustment Factor', None),
                ('Interception Fraction', None),
                ('Surface Loss Coefficient', 'kp_unit'),
                ('Exposure Length', 'Tp_unit'),
                ('Standing Biomass', 'Yp_unit')
            ]
        ).drop(
            columns=['variable_2']
        ).rename(columns={
            'product': 'Product',
            'variable_1': 'Parameter Name',
            'value_1': 'Value',
            'value_2': 'Unit'
        })
        return pps

    def make_animal_ir_report():
        animal_irs = pd.DataFrame(
            get_animal_ingestion_rates(scenario)
        ).drop(
            columns=['consumer_id', 'product_id']
        )[[  # reorder
            'consumer',
            'product',
            'rate',
            'unit',
            'fraction_contaminated',
            'notes'
        ]].rename(columns={
            'consumer': 'Consumer',
            'product': 'Feed Type',
            'fraction_contaminated': 'Fraction Contaminated',
            'rate': 'Ingestion Rate (IR)',
            'unit': 'IR Unit',
            'notes': 'Notes'
        })
        return animal_irs

    def make_bmp_report():
        bmps = get_breast_milk_parameters(scenario)
        if bmps:
            bmps = pd.DataFrame(
                [bmps]
            ).rename(columns={
                'f_mbm': 'Fraction Fat',
                'f_fm': 'Fraction of Maternal Weight in Fat',
                'f_pm': 'Fraction of Maternal Weight in Plasma',
                't_pn': 'Maternal Exposure Duration'
            }).melt(
                id_vars=['t_pn_unit']
            )[[  # reorder
                'variable',
                'value',
                't_pn_unit'
            ]].rename(columns={
                'variable': 'Parameter Name',
                'value': 'Value',
                't_pn_unit': 'Unit'
            })
            bmps.loc[
                bmps['Parameter Name'] != 'Maternal Exposure Duration',
                'Unit'
            ] = pd.NA
        else:
            bmps = pd.DataFrame()
        return bmps

    def make_lf_report():
        lfs = pd.DataFrame(
            get_loss_factors(scenario)
        ).drop(
            columns=['product_id']
        )[[  # reorder
            'product',
            'loss_description',
            'fraction_lost',
            'source'
        ]].rename(columns={
            'product': 'Product',
            'loss_description': 'Loss Description',
            'fraction_lost': 'Fraction Lost',
            'source': 'Source'
        })
        return lfs

    def make_cp_report():
        cps = pd.DataFrame(
            get_chemical_parameters(scenario)
        ).drop(
            columns=['chemical_id']
        ).rename(columns={
            'Fw': 'Fraction Wet Deposition',
            'soil_adjustment': 'Soil Bioavailability',
            'CSF': 'Cancer Slope Factor',
            'RfD': 'Reference Dose'
        })
        cps = multi_melt(
            cps,
            id_vars=['chemical'],
            value_vars=[
                ('Fraction Wet Deposition', None),
                ('Soil Bioavailability', None),
                ('Cancer Slope Factor', 'CSF_unit'),
                ('Reference Dose', 'RfD_unit')
            ]
        ).drop(
            columns=['variable_2']
        ).rename(columns={
            'chemical': 'Chemical',
            'variable_1': 'Parameter Name',
            'value_1': 'Value',
            'value_2': 'Unit'
        })
        return cps

    def make_maf_report():
        mafs = pd.DataFrame(
            get_mutagenic_parameters(scenario)
        ).drop(
            columns=['chemical_id', 'life_stage_id']
        ).rename(columns={
            'chemical': 'Chemical',
            'life_stage': 'Life Stage',
            'value': 'Value',
            'notes': 'Notes'
        })
        return mafs

    def make_baf_report():
        bafs = pd.DataFrame(
            get_baf_parameters(scenario)
        ).drop(
            columns=['chemical_id', 'aquatic_type_id']
        ).rename(columns={
            'chemical': 'Chemical',
            'aquatic_type': 'Aquatic Type',
            'value': 'Value',
            'unit': 'Unit',
            'notes': 'Notes'
        })
        return bafs

    def make_pcp_report():
        pcps = pd.DataFrame(
            get_plant_chemical_parameters(scenario)
        ).drop(
            columns=['chemical_id', 'product_id']
        ).rename(columns={
            'Br': 'Plant-Soil Bioconcentration Factor',
            'VG': 'Empirical Correction Factor',
            'Bv_ag': 'Air-Plant Biotransfer Factor',
            'RCF': 'Root Concentration Factor'
        })
        pcps = multi_melt(
            pcps,
            id_vars=['chemical', 'product'],
            value_vars=[
                ('Plant-Soil Bioconcentration Factor', None),
                ('Empirical Correction Factor', None),
                ('Air-Plant Biotransfer Factor', None),
                ('Root Concentration Factor', 'RCF_unit')
            ]
        ).drop(
            columns=['variable_2']
        ).rename(columns={
            'chemical': 'Chemical',
            'product': 'Plant',
            'variable_1': 'Parameter Name',
            'value_1': 'Value',
            'value_2': 'Unit',
            'notes': 'Notes'
        })
        pcps.Plant = pcps.Plant.str.title()
        return pcps

    def make_acp_report():
        acps = pd.DataFrame(
            get_animal_chemical_parameters(scenario)
        ).drop(
            columns=['chemical_id', 'product_id']
        ).rename(columns={
            'Bs': 'Soil Bioavailability Factor',
            'MF': 'Metabolism Factor',
            'cooking_adjustment': 'Cooking Adjustment Factor',
            'Ba': 'Biotransfer Factor'
        })
        acps = multi_melt(
            acps,
            id_vars=['chemical', 'product'],
            value_vars=[
                ('Soil Bioavailability Factor', None),
                ('Metabolism Factor', None),
                ('Cooking Adjustment Factor', None),
                ('Biotransfer Factor', 'Ba_unit')
            ]
        ).drop(
            columns=['variable_2']
        ).rename(columns={
            'chemical': 'Chemical',
            'product': 'Animal',
            'variable_1': 'Parameter Name',
            'value_1': 'Value',
            'value_2': 'Unit',
            'notes': 'Notes'
        })
        acps.Animal = acps.Animal.str.title()
        return acps

    def make_bmcp_report():
        bmcps = pd.DataFrame(
            get_breast_milk_chemical_parameters(scenario)
        ).drop(
            columns=['chemical_id', 'product_id']
        ).rename(columns={
            'AE_inf': 'Infant Absorption Efficiency',
            'AE_mat': 'Maternal Absorption Efficiency',
            'f_bl': 'Fraction in Maternal Blood',
            'f_f': 'Fraction in Maternal Fat',
            'f_pl': 'Fraction in Maternal Plasma',
            'h_bm': 'Half-Life in Blood',
            'k_elim': 'Non-Lactating Elimination Rate',
            'k_aq_elac': 'Lactating Elimination Rate',
            'PC_pl_aq': 'Blood-Milk Partition Coefficient',
            'PC_rbc_pl': 'Blood Cell-Plasma Partition Coefficient',
        })
        bmcps = multi_melt(
            bmcps,
            id_vars=['chemical', 'product'],
            value_vars=[
                ('Infant Absorption Efficiency', None),
                ('Maternal Absorption Efficiency', None),
                ('Fraction in Maternal Blood', None),
                ('Fraction in Maternal Fat', None),
                ('Fraction in Maternal Plasma', None),
                ('Half-Life in Blood', 'h_bm_unit'),
                ('Non-Lactating Elimination Rate', 'k_elim_unit'),
                ('Lactating Elimination Rate', 'k_aq_elac_unit'),
                ('Blood-Milk Partition Coefficient', 'PC_pl_aq_unit'),
                ('Blood Cell-Plasma Partition Coefficient', 'PC_rbc_pl_unit')
            ]
        ).drop(
            columns=['variable_2', 'product']
        ).rename(columns={
            'chemical': 'Chemical',
            'variable_1': 'Parameter Name',
            'value_1': 'Value',
            'value_2': 'Unit',
            'notes': 'Notes'
        })
        return bmcps

    report = {
        # Human Parameters
        'Human Ingestion Rates': make_ir_report(),
        'Human Body Weight': make_bw_report(),

        # Product Parameters
        'Human Food Parameters': make_hfp_report(),
        'Plant Parameters': make_pp_report(),
        'Animal Ingestion Rates': make_animal_ir_report(),
        'Breast Milk-Specific Parameters': make_bmp_report(),
        'Loss Factors': make_lf_report(),

        # Chemical Parameters
        'General Chemical Parameters': make_cp_report(),
        'Mutagenic Adjustment Factors': make_maf_report(),
        'Bio-Accumulation Parameters': make_baf_report(),
        'Plant-Chemical Parameters': make_pcp_report(),
        'Animal-Chemical Parameters': make_acp_report(),
        'Breast Milk-Chemical Parameters': make_bmcp_report()
    }

    return report
