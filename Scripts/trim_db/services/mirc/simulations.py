from sqlalchemy.exc import IntegrityError
from mirc_core import calculate_c_product, assess_risk
from ...schema.mirc.simulations.models import *
from ..generic import GenericService, PermissionsMixin
from ..entities import ChemicalService
from ..users import UserService
from .builtins import MircProductService, MircPercentileService
from .utils import *

__all__ = ['MircScenarioService', 'MircSimulationService']


class MircScenarioService(GenericService[MircScenario], PermissionsMixin):
    __model__ = MircScenario

    def __init__(self, model, *args, **kwargs):
        self.__instance = model

    def user_permissions(self):
        scenario = self.__instance
        users = {
            u: scenario.access_level(u)
            for u in UserService.get_all() if u.can('view', scenario, ignore_superuser=True)
        }
        return users

    @classmethod
    def from_form(cls, form, owner=None):
        s = MircScenario(
            name=form.name.data,
            parent_id=form.parent.data,
            notes=form.notes.data
        )

        if owner is not None:
            # Commit now to auto-create an access model for this scenario
            cls.db.session.add(s)
            cls.commit()
            try:
                cls.grant(s, owner, 'manage')
                cls.commit()
            except IntegrityError:
                pass

        return s

    def update_from_form(self, form):
        scenario = self.__instance
        db = MircScenarioService.db
        for ir in form.human_ingestion_parameters:
            updated = update_parameter(
                scenario, ir,
                'IR', 'ingestion rate',
                food=int(ir.product_id.data),
                life_stage=int(ir.life_stage_id.data),
                percentile=int(ir.percentile_id.data),
                value_name='rate'
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, ir,
                'FC', 'fraction contaminated',
                media=int(ir.product_id.data),
                value_name='fraction_contaminated',
                unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)

        for bw in form.body_weight_parameters:
            updated = update_parameter(
                scenario, bw,
                'BW', 'body weight',
                life_stage=int(bw.life_stage_id.data),
                percentile=int(bw.percentile_id.data)
            )
            if updated is not None:
                db.session.add(updated)

        for param in form.product_parameters:
            updated = update_parameter(
                scenario, param,
                'EF', 'exposure frequency',
                media=int(param.product_id.data),
                value_name='EF', unit_name='EF_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)

        for param in form.plant_parameters:
            updated = update_parameter(
                scenario, param,
                'MAF', 'moisture adjustment factor',
                media=int(param.product_id.data),
                value_name='MAF', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'Rp', 'interception fraction',
                media=int(param.product_id.data),
                value_name='Rp', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'kp', 'surface loss coefficient',
                media=int(param.product_id.data),
                value_name='kp', unit_name='kp_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'Tp', 'exposure length',
                media=int(param.product_id.data),
                value_name='Tp', unit_name='Tp_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'Yp', 'standing biomass',
                media=int(param.product_id.data),
                value_name='Yp', unit_name='Yp_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)

        for ir in form.animal_ingestion_parameters:
            updated = update_parameter(
                scenario, ir,
                'IR', 'ingestion rate',
                media=int(ir.consumer_id.data),
                food=int(ir.product_id.data),
                value_name='rate'
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, ir,
                'FC', 'fraction contaminated',
                media=int(ir.product_id.data),
                value_name='fraction_contaminated',
                unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)

        bm = MircProductService.get(name='breast milk')
        if bm is not None:
            updated = update_parameter(
                scenario, form.breast_milk_parameters,
                'f_mbm', 'fraction breast milk fat',
                media=bm.id,
                value_name='f_mbm',
                unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, form.breast_milk_parameters,
                'f_fm', 'fraction maternal weight fat',
                media=bm.id,
                value_name='f_fm',
                unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, form.breast_milk_parameters,
                'f_pm', 'fraction maternal weight plasma',
                media=bm.id,
                value_name='f_pm',
                unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, form.breast_milk_parameters,
                't_pn', 'maternal exposure duration',
                media=bm.id,
                value_name='t_pn',
                unit_name='t_pn_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)

        lfs = {}
        for lf in form.product_loss_parameters:
            if lf.product_id.data not in lfs:
                lfs[lf.product_id.data] = []
            if (
                lf.loss_description.data is None
                or not lf.loss_description.data.strip()
            ):
                continue
            lfs[lf.product_id.data].append(lf.data)
        for product_id, lf_list in lfs.items():
            db_lfs = scenario.parameters.for_media(int(product_id)).LF
            if not isinstance(db_lfs, list):
                db_lfs = [db_lfs]
            new_lfs = {lf['loss_description']: lf for lf in lf_list}
            for db_lf in db_lfs:
                if not db_lf:
                    continue
                if db_lf.name in new_lfs:
                    lf = new_lfs[db_lf.name]
                    if (
                        lf['fraction_lost'] != db_lf.value
                        or lf['source'] != db_lf.source
                    ):
                        if db_lf.scenario.id == scenario.id:
                            db_lf.value = lf['fraction_lost']
                            db_lf.source = lf['source']
                        else:
                            new_lf = MircSimulationParameter(
                                scenario=scenario,
                                media=db_lf.media,
                                name=db_lf.name,
                                variable=db_lf.variable,
                                value=lf['fraction_lost'],
                                source=lf['source']
                            )
                            db.session.add(new_lf)
                    del new_lfs[db_lf.name]
                else:
                    add_lf = False
                    if db_lf.scenario.id == scenario.id:
                        nm = db_lf.name
                        db.session.delete(db_lf)
                        if scenario.parent:
                            parent_lfs = scenario.parent.parameters.for_media(
                                product_id
                            ).LF
                            if not isinstance(parent_lfs, list):
                                parent_lfs = [parent_lfs]
                            if len([x for x in parent_lfs if x and x.name == nm]):
                                add_lf = True
                    else:
                        add_lf = True
                    if add_lf:
                        empty_lf = MircSimulationParameter(
                            scenario=scenario,
                            media=db_lf.media,
                            name=db_lf.name,
                            variable=db_lf.variable,
                            value=0,
                            source=''
                        )
                        db.session.add(empty_lf)
            for name, lf in new_lfs.items():
                new_lf = MircSimulationParameter(
                    scenario=scenario,
                    media_id=product_id,
                    name=name,
                    variable='LF',
                    value=lf['fraction_lost'],
                    source=lf['source']
                )
                db.session.add(new_lf)

        for param in form.chemical_parameters:
            updated = update_parameter(
                scenario, param,
                'Fw', 'fraction wet deposition',
                chemical=int(param.chemical_id.data),
                value_name='Fw', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'SoilAdjFactor', 'soil bioavailability factor',
                chemical=int(param.chemical_id.data),
                value_name='soil_adjustment', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'CSF', 'cancer slope factor',
                chemical=int(param.chemical_id.data),
                value_name='CSF', unit_name='CSF_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'RfD', 'reference dose',
                chemical=int(param.chemical_id.data),
                value_name='RfD', unit_name='RfD_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)

        for param in form.mutagenic_parameters:
            updated = update_parameter(
                scenario, param,
                'ADAF', 'mutagenic age-dependent adjustment factor',
                chemical=int(param.chemical_id.data),
                life_stage=int(param.life_stage_id.data),
                unit_name=None
            )
            if updated is not None:
                db.session.add(updated)

        for param in form.baf_parameters:
            var = 'BAF'
            nm = 'bioaccumulation factor'
            if 'BSAF' in param.aquatic_type.data:
                var = 'BSAF'
                nm = 'biota sediment accumulation factor'
            updated = update_parameter(
                scenario, param,
                var, nm,
                chemical=int(param.chemical_id.data),
                media=int(param.aquatic_type_id.data)
            )
            if updated is not None:
                db.session.add(updated)

        for param in form.plant_chemical_parameters:
            updated = update_parameter(
                scenario, param,
                'Br', 'plant-soil bioconcentration factor',
                chemical=int(param.chemical_id.data),
                media=int(param.product_id.data),
                value_name='Br', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'VG', 'empirical correction factor',
                chemical=int(param.chemical_id.data),
                media=int(param.product_id.data),
                value_name='VG', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'Bv_ag', 'air-plant biotransfer factor',
                chemical=int(param.chemical_id.data),
                media=int(param.product_id.data),
                value_name='Bv_ag', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'RCF', 'root concentration factor',
                chemical=int(param.chemical_id.data),
                media=int(param.product_id.data),
                value_name='RCF', unit_name='RCF_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)

        for param in form.animal_chemical_parameters:
            updated = update_parameter(
                scenario, param,
                'Bs', 'soil bioavailability factor',
                chemical=int(param.chemical_id.data),
                media=int(param.product_id.data),
                value_name='Bs', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'MF', 'metabolism factor',
                chemical=int(param.chemical_id.data),
                media=int(param.product_id.data),
                value_name='MF', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'FishAdjFactor', 'fish cooking adjustment factor',
                chemical=int(param.chemical_id.data),
                media=int(param.product_id.data),
                value_name='cooking_adjustment', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'Ba', 'biotransfer factor',
                chemical=int(param.chemical_id.data),
                media=int(param.product_id.data),
                value_name='Ba', unit_name='Ba_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)

        for param in form.breast_milk_chemical_parameters:
            updated = update_parameter(
                scenario, param,
                'AE_inf', 'infant absorption efficiency',
                chemical=int(param.chemical_id.data),
                media=bm.id,
                value_name='AE_inf', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'AE_mat', 'maternal absorption efficiency',
                chemical=int(param.chemical_id.data),
                media=bm.id,
                value_name='AE_mat', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'f_bl', 'fraction in maternal blood',
                chemical=int(param.chemical_id.data),
                media=bm.id,
                value_name='f_bl', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'f_f', 'fraction in maternal fat',
                chemical=int(param.chemical_id.data),
                media=bm.id,
                value_name='f_f', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'f_pl', 'fraction in maternal plasma',
                chemical=int(param.chemical_id.data),
                media=bm.id,
                value_name='f_pl', unit_name=None,
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'h_bm', 'half life',
                chemical=int(param.chemical_id.data),
                media=bm.id,
                value_name='h_bm', unit_name='h_bm_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'k_elim', 'non-lactating elimination rate constant',
                chemical=int(param.chemical_id.data),
                media=bm.id,
                value_name='k_elim', unit_name='k_elim_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'k_aq_elac', 'lactating elimination rate',
                chemical=int(param.chemical_id.data),
                media=bm.id,
                value_name='k_aq_elac', unit_name='k_aq_elac_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'PC_pl_aq', 'blood-milk partition coefficient',
                chemical=int(param.chemical_id.data),
                media=bm.id,
                value_name='PC_pl_aq', unit_name='PC_pl_aq_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)
            updated = update_parameter(
                scenario, param,
                'PC_rbc_pl', 'blood cell-plasma partition coefficient',
                chemical=int(param.chemical_id.data),
                media=bm.id,
                value_name='PC_rbc_pl', unit_name='PC_rbc_pl_unit',
                with_notes=False
            )
            if updated is not None:
                db.session.add(updated)

        db.session.commit()


SIMULATION_PARAMETER_ABBRS = [
    'Ca', 'Fv', 'rho_a', 'C_water', 'C_soil', 'C_root_veg',
    'Kd', 'Cs_s', 'Kd_feed', 'Cs_root_zone', 'Drdp', 'Drwp',
    'C_sed', 'C_surf_water', 'FMD'
]
SIMULATION_PARAMETER_DEFAULTS = {
    'Ca': 0, 'Fv': 0, 'rho_a': 1
}

SIMULATION_PERCENTILE_PRESETS = [
    'farmer', 'fisher', 'farmer_fisher',
    'urban_gardener', 'rural_gardener',
    'custom'
]


class MircSimulationService(GenericService[MircSimulation]):
    __model__ = MircSimulation

    @classmethod
    def from_form(cls, trim_scenario, form):
        i = len(trim_scenario.mirc_simulations) + 1
        sim = cls.create(
            name=f'Simulation {i}',
            trim_scenario_id=trim_scenario.id,
            mirc_scenario=MircScenarioService.get(form.mirc_scenario.data),
            chemical=ChemicalService.get(form.chemical.data),
            use_baf=(form.fish_factor.data == 'baf')
        )

        sim.percentiles.append(MircSimulationPercentile(
            percentile_id=form.human_body_weight_percentile.data
        ))

        sim.parameters.append(MircSimulationParameter(
            variable='percentile_preset',
            value=SIMULATION_PERCENTILE_PRESETS.index(form.ingestion_percentile_preset.data)
        ))

        for p in MircProductService.get_all():
            attr = f'{p.name.lower().replace(" ", "_")}_percentile'
            if hasattr(form, attr):
                sim.percentiles.append(MircSimulationPercentile(
                    food=p,
                    percentile_id=getattr(form, attr).data
                ))
            if p.is_a('fish') and p.name != 'fish':
                f = 0
                src = ''
                tl35_type = form.trim_fish_tl35_compartment.data.split(' in ')[0].replace('_', ' ').lower()
                tl4_type = form.trim_fish_tl4_compartment.data.split(' in ')[0].replace('_', ' ').lower()
                if p.name == tl35_type:
                    f = form.f_tl35.data
                    src = form.f_tl35_src.data
                    sim.parameters.append(MircSimulationParameter(
                        name=form.C_tl35.label.text,
                        variable=f'C_{p.name.replace(" ", "_")}',
                        value=form.C_tl35.data,
                        unit=form.C_tl35_unit.data,
                        source=form.trim_fish_tl35_compartment.data
                    ))
                elif p.name == tl4_type:
                    f = form.f_tl4.data
                    src = form.f_tl4_src.data
                    sim.parameters.append(MircSimulationParameter(
                        name=form.C_tl4.label.text,
                        variable=f'C_{p.name.replace(" ", "_")}',
                        value=form.C_tl4.data,
                        unit=form.C_tl4_unit.data,
                        source=form.trim_fish_tl4_compartment.data
                    ))
                if f != 0:
                    sim.consumption_breakdowns.append(
                        MircSimulationConsumptionBreakdown(
                            subfood=p,
                            fraction=f,
                            source=src
                        )
                    )

        for param in SIMULATION_PARAMETER_ABBRS:
            if not hasattr(form, param):
                continue
            field = getattr(form, param)
            val = field.data
            if val is None:
                if param in SIMULATION_PARAMETER_DEFAULTS:
                    val = SIMULATION_PARAMETER_DEFAULTS[param]
                else:
                    continue
            unit = None
            if hasattr(form, f'{param}_unit'):
                unit = getattr(form, f'{param}_unit').data
            src = None
            if hasattr(form, f'{param}_src'):
                src = getattr(form, f'{param}_src').data
            sim.parameters.append(MircSimulationParameter(
                name=field.label.text,
                variable=param,
                value=val,
                unit=unit,
                source=src
            ))

        return sim

    def __init__(self, model, *args, **kwargs):
        self.__instance = model

    def run_pathways(self):
        simulation = self.__instance
        scenario = simulation.mirc_scenario
        logs = []
        logs.append(f'Loaded {scenario}')

        products = MircProductService.get_all()
        products = [
            p for p in products
            if p.is_food and p.name != 'breast milk'
            and scenario.parameters.for_food(p).IR
        ]
        logs.append(f'Loaded products: {products}')

        bm = MircProductService.get(name='breast milk')
        with_breast_milk = (scenario.parameters.for_food(bm).IR or False)
        Pmean = MircPercentileService.get(name='Pmean')

        c = simulation.chemical
        logs.append(f'Loaded {c}')

        bw = [
            pct for pct in simulation.percentiles
            if pct.food is None
        ]
        if bw:
            bw = bw[0].percentile
        else:
            bw = Pmean

        simulation_breakdown = {}

        simulation_breakdown = {
            p.name.replace(' ', '_'): self._run_single_pathway(p, bw, logs)
            for p in products
        }

        if with_breast_milk:
            cumulative_ladd = 0
            # loop to computed cumulative LADD
            # that is used to estimate BM concentrations
            for product, result in simulation_breakdown.items():
                r = result['risk']
                life_risk = r['Lifetime']
                if life_risk:
                    cumulative_ladd += life_risk.get('intake', 0)

            simulation_breakdown[bm.name.replace(' ', '_')] = self._run_single_pathway(
                bm, bw, logs, maternal_cumulative_ladd=cumulative_ladd
            )

        total = {}
        for product, results in simulation_breakdown.items():
            if not results.get('risk'):
                continue
            for age, risk_data in results['risk'].items():
                if not total.get(age):
                    ureg = scenario.parameters.unit_registry
                    total[age] = {
                        'intake': 0 * ureg('mg/day/kg')
                    }
                total[age]['intake'] += (risk_data.get('intake') or 0)
                adj = risk_data.get('adjusted_intake')
                if adj is not None:
                    if not total[age].get('adjusted_intake'):
                        ureg = scenario.parameters.unit_registry
                        total[age]['adjusted_intake'] = 0 * ureg('mg/day/kg')
                    total[age]['adjusted_intake'] += adj

        RfD = scenario.parameters.for_chemical(c).RfD.quantity
        CSF = scenario.parameters.for_chemical(c).CSF.quantity
        for age, risk in total.items():
            if c.mutagenic:
                i = risk['adjusted_intake']
            else:
                i = risk['intake']

            if RfD:
                risk['hazard_quotient'] = i / RfD
            if CSF and age == 'Lifetime':
                risk['risk_factor'] = i * CSF

        simulation_results = {
            'total': {'risk': total},
            **simulation_breakdown
        }

        print(simulation.parameters)

        return {
            'meta': {
                'importSource': simulation.trim_scenario.name or 'N/A',
                'chemical': simulation.chemical.as_serializable(),
                'fishPathway': 'B(S)AF' if simulation.use_baf else 'Direct',
                'percentiles': {
                    p.food.name.replace(' ', '_') if p.food else 'body_weight':
                    p.percentile.name
                    for p in simulation.percentiles
                },
                'other_parameters': [p.as_serializable() for p in simulation.parameters]
            },
            'results': simulation_results,
            'logs': logs
        }

    def _run_single_pathway(
        self, product, body_weight, logs,
        maternal_cumulative_ladd=None
    ):
        logs.append(f'Calculating {product.name} concentration ...')

        simulation = self.__instance
        scenario = simulation.mirc_scenario

        is_bm = product.name.lower() == 'breast milk'
        if is_bm:
            c_fat, c_aq = calculate_c_product(
                scenario=scenario, product=product, chemical=simulation.chemical,
                simulation=simulation,
                maternal_cumulative_ladd=maternal_cumulative_ladd
            )

            if c_fat is None or c_aq is None:
                c_product = None
            else:
                f_mbm = scenario.parameters.for_media(product).f_mbm.value or .5
                c_product = (c_fat * f_mbm) + (c_aq * (1 - f_mbm))
        else:
            c_product = calculate_c_product(
                scenario=scenario, simulation=simulation,
                product=product, chemical=simulation.chemical,
                logs=logs
            )

        irp = [
            pct for pct in simulation.percentiles
            if pct.food == product
        ]
        if irp:
            irp = irp[0].percentile
        else:
            irp = MircPercentileService.get(name='Pmean')

        logs.append(f'Ingestion Rate Percentile for {product.name} = {irp}')

        logs.append(f'Calculating {product.name} risk ...')
        if is_bm:
            risk_data = assess_risk(
                scenario=scenario,
                product=product, chemical=simulation.chemical,
                concentration_fat=c_fat, concentration_aq=c_aq,
                ingestion_percentile=irp,
                logs=logs
            )
        else:
            risk_data = assess_risk(
                scenario=scenario,
                product=product, chemical=simulation.chemical,
                concentration=c_product,
                ingestion_percentile=irp,
                body_weight_percentile=body_weight,
                logs=logs
            )

        return {
            'concentration': c_product,
            'risk': risk_data
        }
