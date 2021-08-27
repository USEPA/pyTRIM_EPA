import sqlalchemy as sa
from shapely.geometry import Polygon
from ..utils.base import Model


__all__ = [
    'Parcel', 'VolumeElement'
]


class Parcel(Model):
    name = sa.Column(sa.String(120), nullable=False)

    scenario_id = sa.Column(
        sa.Integer(), sa.ForeignKey('scenario.id')
    )
    scenario = sa.orm.relationship('Scenario')

    # Store as a string, but make a property to access as an array
    _vertices = sa.Column('vertices', sa.String(), nullable=False)

    @property
    def vertices(self):
        def strip_brackets(x):
            brackets = '[](){}'
            for b in brackets:
                x = x.replace(b, '')
            return x

        return [
            [
                float(strip_brackets(n.strip()))
                for n in x.split(',')
            ]
            for x in (self._vertices or '').split(';')
        ]

    @vertices.setter
    def vertices(self, value):
        if isinstance(value, str):
            self._vertices = value
        else:
            self._vertices = ';'.join([str(x) for x in value])

    @property
    def polygon(self):
        return Polygon(self.vertices)

    @property
    def area(self):
        return self.polygon.area

    # Each parcel should have a unique name in its scenario
    __table_args__ = (
        sa.UniqueConstraint('scenario_id', 'name'),
    )


class VolumeElement(Model):
    name = sa.Column(sa.String(120), nullable=False)

    parcel_id = sa.Column(
        sa.Integer(), sa.ForeignKey('parcel.id')
    )
    parcel = sa.orm.relationship('Parcel')

    top = sa.Column(sa.Float(), nullable=False)
    bottom = sa.Column(sa.Float(), nullable=False)

    @property
    def height(self):
        return self.top - self.bottom

    @property
    def volume(self):
        return self.parcel.area * self.height

    # Each volume element should have a unique name relative to its parcel
    __table_args__ = (
        sa.UniqueConstraint('parcel_id', 'name'),
    )

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'{self.id}, "{self.name}", "{self.parcel.name}",'
            f' volume={self.volume}'
            ')'
        )


class Compartment(Model):
    name = sa.Column(sa.String(120), nullable=False)

    volume_element_id = sa.Column(
        sa.Integer(), sa.ForeignKey('volume_element.id')
    )
    volume_element = sa.orm.relationship('VolumeElement')

    # Each compartment should have a unique name in its volume element
    __table_args__ = (
        sa.UniqueConstraint('volume_element_id', 'name'),
    )
