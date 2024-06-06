import sqlalchemy as sa
from datetime import datetime
import json

import sqlalchemy.sql.sqltypes

from ..utils.base import Model
from ..utils.mixins import TrackUpdatesMixin
from ..utils.serialize import register_serializer
from ..parameters.models import CustomParameter, ParameterDefinition
from ..entities.models import Chemical


__all__ = [
    'Scenario', 'ScenarioLoadRunProc'
]


class Scenario(Model, TrackUpdatesMixin):
    name = sa.Column(sa.String(120), nullable=False)
    description = sa.Column(sa.String(255))

    @property
    def chemicals(self):
        for c in self._chemicals:
            c.current_scenario(self)
        return self._chemicals

    @chemicals.setter
    def chemicals(self, value):
        self._chemicals = value

    def get_chemical(self, name_or_cas):
        for c in self.chemicals:
            if c.name == name_or_cas or c.cas_number == name_or_cas:
                return c
        return None

    def get_parcel(self, name):
        for p in self.parcels:
            if p.name == name:
                return p
        return None

    @property
    def volume_elements(self):
        volume_els = []
        for p in self.parcels:
            for ve in p.volume_elements:
                ve.current_scenario(self)
                volume_els.append(ve)
        return list(sorted(volume_els, key=lambda x: x.name))

    def get_volume_element(self, name):
        for ve in self.volume_elements:
            if ve.name == name or ve.standard_name == name:
                return ve
        return None

    @property
    def compartments(self):
        comps = []
        for ve in self.volume_elements:
            for c in ve.compartments:
                c.current_scenario(self)
                comps.append(c)
        return list(sorted(comps, key=lambda x: x.name))

    def get_compartment(self, name):
        for c in self.compartments:
            if c.name == name or c.standard_name == name:
                return c
        return None

    @property
    def safe_name(self):
        return self.name.replace(' ', '_')

    @property
    def short_description(self):
        if not self.description:
            return ''

        w = self.description.split()
        w.reverse()
        short = ''
        while len(short) < 75 and len(w):
            short += ' ' + w.pop()
        if len(w):
            short += ' ...'
        return short.strip()

    creator_id = sa.Column(
        sa.Integer(), sa.ForeignKey('user.id'), nullable=False
    )
    creator = sa.orm.relationship(
        'User', backref=sa.orm.backref('created_scenarios', lazy='dynamic')
    )

    # @property
    # def erosion_rate_data_source(self):
    #     opt = 1
    #     try:
    #         opt = self.erosionRateCalcSource
    #     except Exception as ex:
    #         print(f"Erosion rate calculation option not set??\n{ex}")
    #     finally:
    #         return opt

    @property
    def sim_begin_end_time(self):
        # get begin end time param names
        sim_beg = '2001-01-01'
        sim_end = '2010-12-31'
        try:
            sim_beg = datetime.utcfromtimestamp(int(self.simulationBeginDateTime)).strftime('%Y-%m-%d') or sim_beg
            sim_end = datetime.utcfromtimestamp(int(self.simulationEndDateTime)).strftime('%Y-%m-%d') or sim_end
        except Exception as ex:
            # print(f'Problem getting simulation begin and/or end times!\n{ex}')
            sim_beg = '2001-01-01'
            sim_end = '2010-12-31'

        return sim_beg, sim_end

    @property
    def has_process_hist(self):
        try:
            if len([*self.proc_status]) == 0:
                return False
        except Exception:
            return False
        return True

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.name}"'
            ')'
        )


class ScenarioLoadRunProc(Model):
    load_status = sa.Column(sa.String(120))
    run_status = sa.Column(sa.String(120))
    scenario_id = sa.Column(
        sa.Integer(), sa.ForeignKey('scenario.id'), nullable=False
    )
    scenario = sa.orm.relationship(
        'Scenario', backref=sa.orm.backref('proc_status', lazy='dynamic')
    )
    run_datetime = sa.Column(sa.sql.sqltypes.DATETIME)
    result_file_nt = sa.Column(sa.String(255))
    result_file_conc = sa.Column(sa.String(255))
    result_nt = sa.Column(sa.sql.sqltypes.TEXT)
    result_conc = sa.Column(sa.sql.sqltypes.TEXT)

    @property
    def load_percent(self):
        if self.load_status.startswith("loaded"):
            perc = int(self.load_status.split(" ")[1])
        else:
            perc = -1
        return perc

    @property
    def is_load_error(self):
        if self.load_percent == -1:
            return True
        return False

    @property
    def run_step(self):
        if self.run_status.startswith("run"):
            step = self.run_status.split(" ")[1]
            perc = self.run_status.split(" ")[2]
            return step, perc
        return "err"

    @property
    def is_run_error(self):
        if self.run_step == "err":
            return True
        return False


@register_serializer(Scenario)
def serialize_scenario(scen: Scenario):

    def get_wet_interception_params(wi_type, media_name):
        # TODO Need to figure out why agriculture_leaf does not have CalculateWIF
        comps_par = {comp_n: par_dict for comp_n, par_dict in leaf_pars.items() if media_name.replace("_Leaf", "") in comp_n}
        # IMPORTANT: We are assuming all relevant scenario compartments of this type will have the same value.
        # This requires that when this parameter is updated, it is done so for all compartments of this type for
        # this scenario
        pars = {}
        if comps_par:
            pars = comps_par[list(comps_par.keys())[0]]
        wi_data = None
        if wi_type == 1:
            wi_data = safe_get_param_value("WetDepInterceptionFraction_UserSupplied", pars)
        elif wi_type == 2:
            wi_data = safe_get_param_value("CalculateWetDepInterceptionFraction", pars)
        elif wi_type == 3:
            wi_data = safe_get_param_value("WetDepInterceptionFraction_Calculated", pars)
        if wi_data is not None:
            return float(wi_data)
        else:
            return -1

    def get_seasonal_dynamics_params(sd_type, media_name):
        sd_data = None
        comps_par = {comp_n: par_dict for comp_n, par_dict in leaf_pars.items() if
                     media_name.replace("_Leaf", "") in comp_n}
        # IMPORTANT: We are assuming all relevant scenario compartments of this type will have the same value.
        # This requires that when this parameter is updated, it is done so for all compartments of this type for
        # this scenario
        pars = {}
        if comps_par:
            pars = comps_par[list(comps_par.keys())[0]]
        if sd_type == 'lf':
            sd_data = safe_get_param_value("LitterFallRate", pars)
        elif sd_type == 'ae':
            # TODO is allowExchange_forAir correct? should we use _forOther instead?
            #   or should we directly use _Dynamic (which these point to)
            if pars:
                comp = [c for c in scen.compartments if c.standard_name == list(comps_par.keys())[0]]
                sd_data = safe_get_param_value("AllowExchange_forAir", pars, needs_quantity={'comp': comp[0]})
        if sd_data is not None:
            try:
                return float(sd_data)
            except TypeError:
                print(sd_data)
        else:
            return -1

    def get_latest_run_info():
        run_info = {'has_run': scen.has_process_hist,
                    "lastest_run_date": "",
                    "run_has_results": False,
                    "run_results": {}
                    }
        if run_info["has_run"]:
            proc_info = [*scen.proc_status][0]
            run_info["lastest_run_date"] = proc_info.run_datetime
            run_info["run_has_results"] = True if proc_info.run_status == 'run fin 100' else False
            if run_info["run_has_results"]:
                run_info["run_results"] = {
                    "mass_results": f'{{{json.loads(json.dumps(json.loads(proc_info.result_nt), indent=4, sort_keys=True,default=str))}}}',
                    "mass_results_file": proc_info.result_file_nt,
                    "conc_results": f'{{{json.loads(json.dumps(json.loads(proc_info.result_conc), indent=4, sort_keys=True, default=str))}}}',
                    "conc_results_file": proc_info.result_file_conc
                }
        return run_info

    def safe_get_param_value(par_name, par_dict, needs_quantity={}):
        safe_val = None
        if par_name in par_dict:
            if isinstance(par_dict[par_name], CustomParameter):
                if 'unit' in needs_quantity:
                    safe_val = par_dict[par_name].quantity.to(needs_quantity['unit']).magnitude
                else:
                    safe_val = par_dict[par_name].value
                if 'comp' in needs_quantity:
                    safe_val = par_dict[par_name].formula.eval(self=needs_quantity['comp'], environment=scen)
            if isinstance(par_dict[par_name], ParameterDefinition):
                safe_val = par_dict[par_name].default_value
                if 'comp' in needs_quantity:
                    safe_val = par_dict[par_name].default_formula.eval(self=needs_quantity['comp'], environment=scen)

        return safe_val

    scen_pars = {pn: po for pn, po in scen.parameters.items()}

    leaf_pars = {c.standard_name: {pn: p for pn, p in c.parameters.items()} for c in scen.compartments if
                 c.media.isa('$_Leaf')}

    s = {
        'id': scen.id,
        'name': scen.name,
        'description': scen.description,
        'simulation_start_date': scen.sim_begin_end_time[0],
        'simulation_end_date': scen.sim_begin_end_time[1],
        'latest_run_info': get_latest_run_info(),
        'erosionRateSource': safe_get_param_value("erosionRateCalcSource", scen_pars) or 1,
        'scenario_chem': [c.name for c in scen.chemicals],
        'all_chem': [c.name for c in list(Chemical.query.all())],
        'meteo': {
            'ambient_air_temp': safe_get_param_value("AirTemperature", scen_pars, needs_quantity={'unit': "K"}),
            'horizontal_wind_speed': safe_get_param_value("horizontalWindSpeed", scen_pars),
            'wind_dir': safe_get_param_value("windDirection", scen_pars),
            # TODO scen?.mixingHeight??, # it is in Input_files/1Parameters.csv
            # wired to top of Air comp/VE in Foundries_SS (4) Properties.txt,
            'mixing_height': safe_get_param_value("mixingHeight", scen_pars)
            if safe_get_param_value("mixingHeight", scen_pars) else
            [a.height.magnitude for a in scen.compartments if a.media.isa("Air") and "Upper" not in a.standard_name][0],
            'daytime_indicator': safe_get_param_value("isDay_Dynamic", scen_pars),
            'precipitation': safe_get_param_value("Rain", scen_pars),
            'cumulative_precip': safe_get_param_value("cumulativeRain", scen_pars)},
        'wet_dep_interception': {
            'wet_dep_interception_frac_coniferous_leaf': get_wet_interception_params(1, "Coniferous_Leaf"),
            'calc_wet_dep_interception_frac_coniferous_leaf': get_wet_interception_params(2, "Coniferous_Leaf"),
            'wet_dep_interception_frac_coniferous_leaf_calculated': get_wet_interception_params(3, "Coniferous_Leaf"),
            'wet_dep_interception_frac_deciduous_leaf': get_wet_interception_params(1, "Deciduous_Leaf"),
            'calc_wet_dep_interception_frac_deciduous_leaf': get_wet_interception_params(2, "Deciduous_Leaf"),
            'wet_dep_interception_frac_deciduous_leaf_calculated': get_wet_interception_params(3, "Deciduous_Leaf"),
            'wet_dep_interception_frac_grass_leaf': get_wet_interception_params(1, "Grass_Leaf"),
            'calc_wet_dep_interception_frac_grass_leaf': get_wet_interception_params(2, "Grass_Leaf"),
            'wet_dep_interception_frac_grass_leaf_calculated': get_wet_interception_params(3, "Grass_Leaf"),
            'wet_dep_interception_frac_agriculture_leaf': get_wet_interception_params(1, "Agriculture_Leaf"),
            'calc_wet_dep_interception_frac_agriculture_leaf': get_wet_interception_params(2, "Agriculture_Leaf"),
            'wet_dep_interception_frac_agriculture_leaf_calculated': get_wet_interception_params(3, "Agriculture_Leaf")
        },
        'seasonal_dynamics': {
            'litterfall_coniferous': get_seasonal_dynamics_params('lf', 'Coniferous_Leaf'),
            'allow_exchange_coniferous': get_seasonal_dynamics_params('ae', 'Coniferous_Leaf'),
            'litterfall_deciduous': get_seasonal_dynamics_params('lf', 'Deciduous_Leaf'),
            'allow_exchange_deciduous': get_seasonal_dynamics_params('ae', 'Deciduous_Leaf'),
            'litterfall_grass': get_seasonal_dynamics_params('lf', 'Grass_Leaf'),
            'allow_exchange_grass': get_seasonal_dynamics_params('ae', 'Grass_Leaf'),
            'litterfall_agriculture': get_seasonal_dynamics_params('lf', 'Agriculture_Leaf'),
            'allow_exchange_agriculture': get_seasonal_dynamics_params('ae', 'Agriculture_Leaf')
        }
    }
    return s
