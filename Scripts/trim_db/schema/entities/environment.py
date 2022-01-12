import json
import sqlalchemy as sa
from shapely.geometry import Polygon
from ..parameters.utils import ureg
from ..utils.base import Model


__all__ = [
    'Parcel', 'VolumeElement', 'Media', 'Compartment',
    'CompartmentLink'
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
        # CAREFUL: we assume dimensions are in meters ...
        return self.polygon.area * ureg('m^2')

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
                comps.append(c)
        return list(sorted(comps, key=lambda x: x.name))

    def get_compartment(self, name=None, media=None):
        if name is None and media is None:
            raise ValueError('Must supply either "name" or "media" argument')
        if media is not None:
            check = [c for c in self.compartments if c.media.isa(media)]
            if name is None:
                return check
        else:
            check = self.compartments
        for x in check:
            if x.name == name or x.standard_name == name:
                return x
        return None

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
            f'"{self.name}", area={self.area}'
            ')'
        )


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
    def standard_name(self):
        return f'{self.name}_{self.parcel.name}'

    @property
    def height(self):
        # CAREFUL: we assume dimensions are in meters ...
        return (self.top - self.bottom) * ureg('m')

    @property
    def volume(self):
        return self.parcel.area * self.height

    def overlap_with(self, volume_element):
        polygon_a = self.parcel.polygon
        polygon_b = volume_element.parcel.polygon

        is_neighbor = polygon_a.intersects(polygon_b)
        if not is_neighbor:
            return 0 * ureg('m^3')

        intersection = polygon_a.intersection(polygon_b)
        xy_overlap = intersection.area
        if xy_overlap == 0:
            # the borders must just touch
            xy_overlap = intersection.length

        top_a = self.top
        top_b = volume_element.top

        bottom_a = self.bottom
        bottom_b = volume_element.bottom

        if top_a == bottom_b or top_b == bottom_a:
            z_overlap = 1

        elif top_a >= top_b and top_b > bottom_a:
            z_overlap = top_b - bottom_a

        elif top_b >= top_a and top_a > bottom_b:
            z_overlap = top_a - bottom_b

        else:
            z_overlap = 0

        # CAREFUL: we assume dimensions are in meters ...
        return (z_overlap * xy_overlap) * ureg('m^3')

    def get_compartment(self, name=None, media=None):
        if name is None and media is None:
            raise ValueError('Must supply either "name" or "media" argument')
        if media is not None:
            check = [c for c in self.compartments if c.media.isa(media)]
            if name is None:
                return check
        else:
            check = self.compartments
        for x in check:
            if x.name == name or x.standard_name == name:
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
            f'{self.__class__.__qualname__}("{self.standard_name}")'
        )


class Media(Model):
    name = sa.Column(sa.String(120), unique=True, nullable=False)

    parent_id = sa.Column(
        sa.Integer(),
        sa.ForeignKey('media.id'),
        nullable=True
    )
    parent = sa.orm.relationship(
        'Media',
        remote_side='Media.id',
        backref=sa.orm.backref('submedia', cascade='all, delete-orphan')
    )

    _can_emit = sa.Column(
        'can_emit', sa.Boolean(), nullable=False, default=True
    )
    _can_absorb = sa.Column(
        'can_absorb', sa.Boolean(), nullable=False, default=True
    )

    @property
    def can_emit(self):
        if self.parent is None:
            return self._can_emit
        return self._can_emit and self.parent.can_emit

    @can_emit.setter
    def can_emit(self, value):
        self._can_emit = value

    @property
    def can_absorb(self):
        if self.parent is None:
            return self._can_absorb
        return self._can_absorb and self.parent.can_absorb

    @can_absorb.setter
    def can_absorb(self, value):
        self._can_absorb = value

    @property
    def category(self):
        if self.parent is None:
            return self.name
        return f'{self.parent.category}|{self.name}'

    def isa(self, name_or_media):
        if isinstance(name_or_media, str):
            if name_or_media == self.name or name_or_media == self.category:
                return True
        elif isinstance(name_or_media, Media):
            if name_or_media.id == self.id:
                return True
        else:
            raise TypeError

        if self.parent is not None:
            return self.parent.isa(name_or_media)

        return False

    def as_serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category
        }

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.category}"'
            ')'
        )


class Compartment(Model):
    name = sa.Column(sa.String(120), nullable=False)

    volume_element_id = sa.Column(
        sa.Integer(), sa.ForeignKey('volume_element.id'), nullable=False
    )
    volume_element = sa.orm.relationship(
        'VolumeElement', backref=sa.orm.backref('compartments', lazy='dynamic')
    )

    media_id = sa.Column(
        sa.Integer(), sa.ForeignKey('media.id'), nullable=False
    )
    media = sa.orm.relationship(
        'Media', backref=sa.orm.backref('compartments', lazy='dynamic')
    )

    @property
    def standard_name(self):
        return f'{self.name} in {self.volume_element.standard_name}'

    @property
    def custom_linked_compartments(self):
        return [x.receiver for x in self._links]

    _linked_compartment_cache = {}

    def linked_compartments(self, media=None):
        # Check cache
        if media in self._linked_compartment_cache:
            return self._linked_compartment_cache[media]

        linked = {
            c.id: c for c in self.custom_linked_compartments
            if (media is None or c.media.isa(media))
        }
        linked.update({
            c.id: c for c in self.volume_element.parcel.compartments
            if (
                c != self and self.get_links(c)
                and (media is None or c.media.isa(media))
            )
        })

        linked = list(linked.values())

        # Set cache
        self._linked_compartment_cache[media] = linked

        return linked

    def connects_to(self, compartment):
        if self.volume_element == compartment.volume_element:
            return True  # We're in the same "space"!

        elif self.volume_element.overlap_with(compartment.volume_element) > 0:
            return True  # Our "spaces" overlap!

        elif compartment in self.custom_linked_compartments:
            return True

        # To bad, we just didn't connect
        return False

    def get_links(self, compartment):
        comp_links = [
            x for x in self._links if x.receiver_id == compartment.id
        ]

        if len(comp_links):
            return comp_links

        if self.connects_to(compartment):
            comp_links.append(DummyLink(self, compartment))
        return comp_links

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
        if self.name != self.media.category:
            return (
                f'{self.__class__.__qualname__}('
                f'"{self.standard_name}", "{self.media.category}"'
                ')'
            )
        else:
            return (
                f'{self.__class__.__qualname__}("{self.standard_name}")'
            )


class DummyLink:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.sender.standard_name}" > "{self.receiver.standard_name}"'
            ')'
        )


class CompartmentLink(Model):
    sender_id = sa.Column(
        sa.Integer(), sa.ForeignKey('compartment.id'), nullable=False
    )
    sender = sa.orm.relationship(
        'Compartment',
        foreign_keys=[sender_id],
        backref=sa.orm.backref('_links', lazy='dynamic')
    )

    receiver_id = sa.Column(
        sa.Integer(), sa.ForeignKey('compartment.id'), nullable=False
    )
    receiver = sa.orm.relationship(
        'Compartment',
        foreign_keys=[receiver_id]
    )

    # Each link should be unique
    __table_args__ = (
        sa.UniqueConstraint('sender_id', 'receiver_id'),
    )

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.sender.standard_name}" > "{self.receiver.standard_name}"'
            ')'
        )
