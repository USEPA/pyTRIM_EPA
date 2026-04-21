from mirc_core import calculate_c_product, assess_risk
from ...schema.mirc.simulations.models import *
from ..generic import GenericService, PermissionsMixin
from ..entities import ChemicalService
from ..users import UserService
from .builtins import MircProductService, MircPercentileService

__all__ = ['MircScenarioService', 'MircSimulationService']


class MircScenarioService(GenericService, PermissionsMixin):
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


SIMULATION_PARAMETER_ABBRS = [
    'Ca', 'Fv', 'rho_a', 'C_water', 'C_soil', 'C_root_veg',
    'Kd', 'Cs_s', 'Kd_feed', 'Cs_root_zone', 'Drdp', 'Drwp',
    'C_sed', 'C_surf_water', 'FMD'
]
SIMULATION_PARAMETER_DEFAULTS = {
    'Ca': 0
}

SIMULATION_PERCENTILE_PRESETS = [
    'farmer', 'fisher', 'farmer_fisher',
    'urban_gardener', 'rural_gardener',
    'custom'
]


class MircSimulationService(GenericService):
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
                        variable=f'C_{p.name.replace(" ", "_")}',
                        value=form.C_tl35.data,
                        unit=form.C_tl35_unit.data,
                        source=form.C_tl35_src.data
                    ))
                elif p.name == tl4_type:
                    f = form.f_tl4.data
                    src = form.f_tl4_src.data
                    sim.parameters.append(MircSimulationParameter(
                        variable=f'C_{p.name.replace(" ", "_")}',
                        value=form.C_tl4.data,
                        unit=form.C_tl4_unit.data,
                        source=form.C_tl4_src.data
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
            val = getattr(form, param).data
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

        return {
            'meta': {
                'importSource': simulation.trim_scenario.name or 'N/A',
                'chemical': simulation.chemical.as_serializable(),
                'fishPathway': 'B(S)AF' if simulation.use_baf else 'Direct',
                'percentiles': {
                    p.food.name.replace(' ', '_') if p.food else 'body_weight':
                    p.percentile.name
                    for p in simulation.percentiles
                }
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
