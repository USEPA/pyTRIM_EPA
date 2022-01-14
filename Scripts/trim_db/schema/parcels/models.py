import sqlalchemy as sa
from ..utils.base import Model

__all__ = [
    'Parcel', 'VolumeElement', 'Compartment'
]


class Parcel(Model):
    name = sa.Column(sa.String(120), nullable=False)
    lats = sa.Column(sa.String(1000), nullable=False)
    longs = sa.Column(sa.String(1000), nullable=False)
    landCover = sa.Column(sa.String(120), nullable=False)
    description = sa.Column(sa.String(255))

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

    compartment = sa.orm.relationship(
        'Compartment', backref=sa.orm.backref('created_compartments', lazy='dynamic')
    )

    volume_element = sa.orm.relationship(
        'VolumeElement',  backref=sa.orm.backref('created_volume_elements', lazy='dynamic'))

    def as_serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'lat': self.lats,
            'long': self.longs,
            'landCover': self.landCover,
            'description': self.description
        }


class VolumeElement(Model):
    pass


class Compartment(Model):
    pass
