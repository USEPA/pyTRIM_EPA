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

    def get_compartment(self, name=None, media=None):
        if media is None:
            if name is None:
                raise ValueError(
                    'Must supply either "name" or "media" argument'
                )
            check = self.compartments
        else:
            check = [c for c in self.compartments if c.media.isa(media)]
            if name is None:
                return check
        for x in check:
            if x.name == name or x.standard_name == name:
                return x
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
    def latest_proc_status(self):
        return self.proc_status.order_by(ScenarioLoadRunProc.id.desc()).first()

    @property
    def has_process_hist(self):
        try:
            if self.latest_proc_status is not None:
                return True
        except Exception:
            return False
        return False

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.name}"'
            ')'
        )


@register_serializer(Scenario)
def serialize_scenario(scen: Scenario):
    start_time, end_time = scen.sim_begin_end_time
    s = {
        'id': scen.id,
        'name': scen.name,
        'description': scen.description
    }


class ScenarioLoadRunProc(Model):
    load_status = sa.Column(sa.String(120))
    run_status = sa.Column(sa.String(120))
    scenario_id = sa.Column(
        sa.Integer(), sa.ForeignKey('scenario.id'), nullable=False
    )
    scenario = sa.orm.relationship(
        'Scenario', backref=sa.orm.backref(
            'proc_status', lazy='dynamic', cascade='all, delete-orphan'
        )
    )
    run_datetime = sa.Column(sa.sql.sqltypes.DATETIME)
    result_file_nt = sa.Column(sa.String(255))
    result_file_conc = sa.Column(sa.String(255))
    result_file_tm = sa.Column(sa.String(255))
    result_nt = sa.Column(sa.sql.sqltypes.TEXT)
    result_conc = sa.Column(sa.sql.sqltypes.TEXT)

    execution_arn = sa.Column(sa.String(255))

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
