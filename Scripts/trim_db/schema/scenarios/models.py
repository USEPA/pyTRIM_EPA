import sqlalchemy as sa
from datetime import datetime

import sqlalchemy.sql.sqltypes

from ..utils.base import Model
from ..utils.mixins import TrackUpdatesMixin
from ..utils.serialize import register_serializer


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
    from trim_db.services import ChemicalService

    def get_wet_interception_params(wi_type, media_name):
        # TODO Need to figure out why agriculture_leaf does not have CalculateWIF
        wi_data = []
        if wi_type == 1:
            wi_data = [c.WetDepInterceptionFraction_UserSupplied for c in scen.compartments if c.media.isa(media_name)]
        elif wi_type == 2:
            wi_data = [c.CalculateWetDepInterceptionFraction for c in scen.compartments if c.media.isa(media_name)]
        elif wi_type == 3:
            wi_data = [c.WetDepInterceptionFraction_Calculated for c in scen.compartments if c.media.isa(media_name)]
        if len(wi_data) > 0:
            try:
                return float(wi_data[0].magnitude)
            except AttributeError:
                return float(wi_data[0])
        else:
            return -1

    def get_seasonal_dynamics_params(sd_type, media_name):
        sd_data = []
        if sd_type == 'lf':
            sd_data = list(set([c.LitterFallRate for c in scen.compartments if c.media.isa(media_name)]))
        elif sd_type == 'ae':
            # TODO is allowExchange_forAir correct? should we use _forOther instead?
            #   or should we directly use _Dynamic (which these point to)
            sd_data = list(set([c.AllowExchange_forAir for c in scen.compartments if c.media.isa(media_name)]))
        if len(sd_data) > 0:
            try:
                return float(sd_data[0].magnitude)
            except AttributeError:
                return float(sd_data[0])
        else:
            return -1

    s = {
        'id': scen.id,
        'name': scen.name,
        'description': scen.description,
        'simulation_start_date': scen.sim_begin_end_time[0],
        'simulation_end_date': scen.sim_begin_end_time[1],
        'erosionRateSource': scen.erosionRateCalcSource or 1,
        'scenario_chem': [c.name for c in scen.chemicals],
        'all_chem': [c.name for c in ChemicalService.get_all()],
        'meteo': {
            'ambient_air_temp': scen.AirTemperature.to("K").magnitude,
            'horizontal_wind_speed': scen.horizontalWindSpeed,
            'wind_dir': scen.windDirection,
            # TODO scen?.mixingHeight??, # it is in Input_files/1Parameters.csv
            # wired to top of Air comp/VE in Foundries_SS (4) Properties.txt,
            'mixing_height': scen.mixingHeight if scen.mixingHeight else
            [a.height.magnitude for a in scen.compartments if a.media.isa("Air") and "Upper" not in a.standard_name][0],
            'daytime_indicator': scen.isDay_Dynamic,
            'precipitation': scen.Rain,
            'cumulative_precip': scen.cumulativeRain},
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
