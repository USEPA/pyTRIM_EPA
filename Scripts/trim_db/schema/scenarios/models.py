import sqlalchemy as sa
from ..utils.base import Model
from ..utils.mixins import TrackUpdatesMixin
from ..utils.serialize import register_serializer


__all__ = [
    'Scenario'
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

    @property
    def erosion_rate_data_source(self):
        for cp in self.custom_params:
            if cp.definition.variable_name == "erosionRateCalcSource":
                return cp.value
            else:
                continue
        return 1

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.name}"'
            ')'
        )


@register_serializer(Scenario)
def serialize_scenario(scen: Scenario):
    s = {
        'id': scen.id,
        'name': scen.name,
        'description': scen.description,
        'erosionRateSource': scen.erosion_rate_data_source
    }
    return s
