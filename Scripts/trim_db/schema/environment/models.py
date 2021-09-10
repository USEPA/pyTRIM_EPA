import json
import sqlalchemy as sa
from shapely.geometry import Polygon
from ..parameters.utils import use_linked_parameters
from ..utils.base import Model


__all__ = [
    'Parcel', 'VolumeElement', 'Compartment'
]


class Parcel(Model):
    name = sa.Column(sa.String(120), nullable=False)

    scenario_id = sa.Column(
        sa.Integer(), sa.ForeignKey('scenario.id'), nullable=False
    )
    scenario = sa.orm.relationship(
        'Scenario', backref=sa.orm.backref('parcels', lazy='dynamic')
    )

    # Store as a string, but make a property to access as an array
    _vertices = sa.Column('vertices', sa.JSON(), nullable=False)

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
                self._vertices = value
            except json.JSONDecodeError:
                raise
        else:
            self._vertices = value

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

    def as_serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'vertices': self.vertices,
            'area': self.area
        }

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'{self.id}, "{self.name}", area={self.area}'
            ')'
        )


@use_linked_parameters
class VolumeElement(Model):
    name = sa.Column(sa.String(120), nullable=False)

    parcel_id = sa.Column(
        sa.Integer(), sa.ForeignKey('parcel.id'), nullable=False
    )
    parcel = sa.orm.relationship(
        'Parcel', backref=sa.orm.backref('volume_elements', lazy='dynamic')
    )

    top = sa.Column(sa.Float(), nullable=False)
    bottom = sa.Column(sa.Float(), nullable=False)

    @property
    def height(self):
        return self.top - self.bottom

    @property
    def volume(self):
        return self.parcel.area * self.height

    def overlap_with(self, volume_element):
        polygon_a = self.parcel.polygon
        polygon_b = volume_element.parcel.polygon

        is_neighbor = polygon_a.intersects(polygon_b)
        if not is_neighbor:
            return 0

        top_a = self.top
        top_b = volume_element.top

        bottom_a = self.bottom
        bottom_b = volume_element.bottom

        xy_overlap = polygon_a.intersection(polygon_b).area

        if top_a == bottom_b or top_b == bottom_a:
            z_overlap = 1

        elif top_a >= top_b and top_b > bottom_a:
            z_overlap = top_b - bottom_a

        elif top_b >= top_a and top_a > bottom_b:
            z_overlap = top_a - bottom_b

        else:
            z_overlap = 0

        return z_overlap * xy_overlap

    def get_compartment(self, name):
        for x in self.compartments:
            if x.name == name:
                return x
        return None

    # Each volume element should have a unique name relative to its parcel
    __table_args__ = (
        sa.UniqueConstraint('parcel_id', 'name'),
    )

    def as_serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'top': self.top,
            'bottom': self.bottom,
            'volume': self.volume
        }

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'{self.id}, "{self.name}", "{self.parcel.name}",'
            f' volume={self.volume}'
            ')'
        )


@use_linked_parameters
class Compartment(Model):
    name = sa.Column(sa.String(120), nullable=False)

    volume_element_id = sa.Column(
        sa.Integer(), sa.ForeignKey('volume_element.id'), nullable=False
    )
    volume_element = sa.orm.relationship(
        'VolumeElement', backref=sa.orm.backref('compartments', lazy='dynamic')
    )

    @property
    def full_name(self):
        return f'{self.name} in {self.volume_element.name}'

    # Each compartment should have a unique name in its volume element
    __table_args__ = (
        sa.UniqueConstraint('volume_element_id', 'name'),
    )

    def as_serializable(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'{self.id}, "{self.name}", "{self.volume_element.name}"'
            ')'
        )
