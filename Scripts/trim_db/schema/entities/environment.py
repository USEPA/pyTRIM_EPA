import json
import pandas as pd
import re
import sqlalchemy as sa
from shapely.geometry import Polygon
from pyproj import CRS, Transformer
from shapely import wkt
from ..parameters.utils import ureg
from ..parameters.models import ParameterDefinition, CustomParameter
from ..utils.base import Model
from ..utils.caching import CacheManager
from ..utils.serialize import register_serializer


__all__ = [
    'Parcel', 'VolumeElement', 'Media', 'Compartment',
    'CompartmentLink'
]

GLOBAL_WILDCARD = "$"


class Parcel(Model):
    name = sa.Column(sa.String(120), nullable=False)
    description = sa.Column(sa.String(250), nullable=True)

    scenario_id = sa.Column(
        sa.Integer(), sa.ForeignKey('scenario.id'), nullable=False
    )
    scenario = sa.orm.relationship(
        'Scenario', backref=sa.orm.backref('parcels')
    )

    # Store as a string, but make a property to access as an array
    _vertices = sa.Column('vertices', sa.JSON(), nullable=False)

    _utm_polygon = None
    _polygon = None
    _area = None

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
        self._utm_polygon = None
        self._polygon = None
        self._area = None

    @property
    def utm_vertices(self):
        # CAREFUL: we assume ellipsoid is WGS84 ..
        proj = (
            'PROJCS['
            '"WGS_1984_UTM_Zone_16N",'
            'GEOGCS['
            '"GCS_WGS_1984",'
            'DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],'
            'PRIMEM["Greenwich",0.0],'
            'UNIT["Degree",0.0174532925199433]'
            '],'
            'PROJECTION["Transverse_Mercator"],'
            'PARAMETER["False_Easting",500000.0],'
            'PARAMETER["False_Northing",0.0],'
            'PARAMETER["Central_Meridian",-87.0],'
            'PARAMETER["Scale_Factor",0.9996],'
            'PARAMETER["Latitude_Of_Origin",0.0],'
            'UNIT["Meter",1.0]'
            ']'
        )
        from_crs = CRS.from_epsg(4326)
        to_crs = CRS.from_wkt(proj)
        transformer = Transformer.from_crs(from_crs, to_crs)
        utm_vert = [transformer.transform(pt[1], pt[0]) for pt in self.vertices]
        return utm_vert

    def polygon(self, utm=True):
        if utm:
            if self._utm_polygon is None:
                self._utm_polygon = Polygon(self.utm_vertices)
            return self._utm_polygon
        if self._polygon is None:
            self._polygon = Polygon(self.vertices)
        return self._polygon

    @property
    def area(self):
        # CAREFUL: we assume dimensions are in meters ...
        if self._area is None:
            self._area = self.polygon().area * ureg('m^2')
        return self._area

    def get_volume_element(self, name):
        for ve in self.volume_elements:
            if ve.name == name or ve.standard_name == name:
                return ve
        return None

    @property
    def compartments(self):
        return list(sorted(
            (c for ve in self.volume_elements for c in ve.compartments),
            key=lambda x: x.name
        ))

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

    # Each parcel should have a unique name in its scenario
    __table_args__ = (
        sa.UniqueConstraint('scenario_id', 'name'),
    )

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.name}", area={self.area}'
            ')'
        )


@register_serializer(Parcel)
def serialize_parcel(pcl: Parcel):
    s = {
        'id': pcl.id,
        'name': pcl.name,
        'description': pcl.description,
        'vertices': pcl.vertices,
        'area': pcl.area.m_as('m^2')
    }
    return s


class VolumeElement(Model):
    name = sa.Column(sa.String(120), nullable=False)

    parcel_id = sa.Column(
        sa.Integer(), sa.ForeignKey('parcel.id'), nullable=False
    )
    parcel = sa.orm.relationship(
        'Parcel', backref=sa.orm.backref('volume_elements')
    )

    top = sa.Column(sa.Float(), nullable=False)
    bottom = sa.Column(sa.Float(), nullable=False)

    @property
    def standard_name(self):
        return f'{self.name}_{self.parcel.name}'

    @property
    def area(self):
        return self.parcel.area

    @property
    def height(self):
        # CAREFUL: we assume dimensions are in meters ...
        return (self.top - self.bottom) * ureg('m')

    @property
    def depth(self):
        return abs(self.height)

    @property
    def volume(self):
        return self.parcel.area * self.height

    def agg(
        self, func, prop, chemical=None, compartment_name=None, compartment_media=None,
        *args, **kwargs
    ):
        comps = self.get_compartment(name=compartment_name, media=compartment_media)
        if not isinstance(comps, list):
            comps = [comps]

        if len(comps) == 0:
            # In this case this method returns 0 but misses the units. Berk added unit for this case on August 19 2024
            from trim_db.services import ParameterService
            par_def = ParameterService.definitions.get(variable_name=prop)
            if par_def.default_unit:
                prop_unit = re.sub(r'\[(.*?)\]', '', par_def.default_unit)
            else:
                prop_unit = ''
            try:
                unit_obj = ureg(prop_unit)
            except Exception as e:
                print(e)
                return 0 * ureg('')
            return 0 * unit_obj

        def get_prop(c):
            if args or kwargs:
                if chemical is not None:
                    return getattr(chemical, prop)(c, *args, **kwargs)
                return getattr(c, prop)(*args, **kwargs)
            else:
                if chemical is not None:
                    return getattr(chemical, prop)(c)
                return getattr(c, prop)

        def eval_prop(c):
            p = get_prop(c)
            if isinstance(p, ParameterDefinition):
                return p.default_value
            elif isinstance(p, CustomParameter):
                return p.value
            else:
                return p

        if func == 'sum':
            props = []
            for c in comps:
                p = eval_prop(c)
                if pd.isna(p):
                    return pd.NA
                props.append(p)
            return sum(props)

        raise AssertionError('Unknown function!')

    # CAREFUL: we assume dimensions are in meters ...
    def interface_with(self, volume_element):
        polygon_a = self.parcel.polygon()
        polygon_b = volume_element.parcel.polygon()

        if not polygon_a.intersects(polygon_b):
            # Not horizontally contiguous
            return 0 * ureg('m^2')

        intersection = polygon_a.intersection(polygon_b)

        # if self.parcel.id == volume_element.parcel.id:
        #     # Total horizontal overlap; same parcel
        #     return self.parcel.area

        top_a = self.top
        top_b = volume_element.top

        bottom_a = self.bottom
        bottom_b = volume_element.bottom

        # OK This bit is tricky... We look for an interface between two volumes so if they have the same parent parcel
        # we still need to check if the top or bottom of these volumes touch or overlap. BUT!!!! we also want
        # pseudosource volume elements to be in touch with all volume elements to be able to transfer the chemicals.
        # In that case we do not have to check bottom and top of those volume elements and checking if they are in the
        # same parcel will be enough. -Berk (06-12-2025)
        if (self.parcel.id == volume_element.parcel.id):
            # volume elements overlap and top/bottom contact
            if ((top_a == bottom_b) or (bottom_a == top_b)):
                # Total horizontal overlap; same parcel
                return self.parcel.area
            # if we are dealing with a source
            if self.name in ["DryParticleSource", "WetParticleSource", "DryVaporSource", "WetVaporSource"]:
                return self.parcel.area

        if top_a < bottom_b or top_b < bottom_a:
            # No vertical overlap
            return 0 * ureg('m^2')

        if top_a > top_b:
            z_side = top_b - bottom_a
        else:
            z_side = top_a - bottom_b

        # if intersection.area > 0:
        #     # Both vertical AND horizontal overlap!
        #     # The interface is actually an area?
        #     return (z_side * intersection.area) * ureg('m^3')

        # Else, only vertical overlap
        xy_side = intersection.length  # Is this arc units?

        return (z_side * xy_side) * ureg('m^2')

    def midpoint_distance(self, volume_element):
        if isinstance(volume_element, Compartment):
            volume_element = volume_element.volume_element

        polygon_a = self.parcel.polygon()
        polygon_b = volume_element.parcel.polygon()

        # CAREFUL: we assume dimensions are in meters ...
        return polygon_a.centroid.distance(polygon_b.centroid) * ureg('m^2')

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

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}("{self.standard_name}")'
        )


@register_serializer(VolumeElement)
def serialize_volume_element(vol: VolumeElement):
    s = {
        'id': vol.id,
        'name': vol.name,
        'top': vol.top,
        'bottom': vol.bottom,
        'volume': vol.volume
    }
    return s


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

    def isa(self, name_or_media, or_child=True):
        if isinstance(name_or_media, str):
            # check wildcard in the beginning
            if name_or_media.startswith(GLOBAL_WILDCARD):
                if (
                        self.name.endswith(name_or_media[1:])
                        or self.category.endswith(name_or_media[1:])
                ):
                    return True
            if name_or_media.endswith(GLOBAL_WILDCARD):
                if (
                        self.name.startswith(name_or_media[:-1])
                        or self.category.startswith(name_or_media[:-1])
                ):
                    return True
            else:
                if (
                    name_or_media == self.name
                    or name_or_media == self.category
                ):
                    return True
        elif isinstance(name_or_media, Media):
            if name_or_media.id == self.id:
                return True
        elif isinstance(name_or_media, list):
            for check in name_or_media:
                if self.isa(check):
                    return True
        else:
            raise TypeError

        if or_child and self.parent is not None:
            return self.parent.isa(name_or_media)

        return False

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.category}"'
            ')'
        )


@register_serializer(Media)
def serialize_media(med: Media):
    s = {
        'id': med.id,
        'name': med.name,
        'category': med.category
    }
    return s


class Compartment(Model):
    name = sa.Column(sa.String(120), nullable=False)

    volume_element_id = sa.Column(
        sa.Integer(), sa.ForeignKey('volume_element.id'), nullable=False
    )
    volume_element = sa.orm.relationship(
        'VolumeElement', backref=sa.orm.backref('compartments')
    )

    media_id = sa.Column(
        sa.Integer(), sa.ForeignKey('media.id'), nullable=False
    )
    media = sa.orm.relationship(
        'Media', backref=sa.orm.backref('compartments')
    )

    @property
    def standard_name(self):
        return f'{self.name} in {self.volume_element.standard_name}'

    @property
    def custom_linked_compartments(self):
        return [x.receiver for x in self._links]

    @property
    def area(self):
        if 'CustomArea' in self.parameters:
            return self.CustomArea
        # By default, assume Compartment.area == volumeElement.area
        # unless BOTH Compartment.volume and Compartment.height are custom
        if (
            'CustomHeight' in self.parameters
            and 'CustomVolume' in self.parameters
        ):
            return self.CustomVolume / self.CustomHeight
        return self.volume_element.area

    @property
    def height(self):
        if 'CustomHeight' in self.parameters:
            return self.CustomHeight
        if 'CustomVolume' in self.parameters:
            # By using Compartment.area,
            # we don't have to check CustomArea here
            return self.CustomVolume / self.area
        return self.volume_element.height

    @property
    def volume(self):
        if 'CustomVolume' in self.parameters:
            return self.CustomVolume
        # Using Compartment.area and Compartment.height
        # makes sure the geometry always makes sense,
        # unless the user has customized all three
        # (area, height, volume),
        # in which case it's their fault if they broke it.
        # The frontend should probably warn them if they try
        return self.area * self.height

    @property
    def depth(self):
        return abs(self.height)

    def linked_compartments(self, media=None, same_parcel=False):
        @CacheManager.with_caching(f'linked_compartments::{self.id}')
        def cached_links(media, same_parcel):
            linked = {
                c.id: c for c in self.custom_linked_compartments
                if (media is None or c.media.isa(media))
            }
            if same_parcel:
                comps = self.volume_element.parcel.compartments
            else:
                comps = self.volume_element.parcel.scenario.compartments
            for c in comps:
                if c.id == self.id:
                    continue
                if (media is not None) and (not c.media.isa(media)):
                    continue
                if self.connects_to(c):
                    linked[c.id] = c
            return list(linked.values())
        return cached_links(media, same_parcel)

    def return_sameparcel_linked_media_id_or_none(self, media=None):
        comps = self.volume_element.parcel.compartments
        for c in comps:
            if c.id == self.id:
                continue
            if (media is not None) and (not c.media.isa(media)):
                continue
            if self.connects_to(c):
                return c.media.id
        return None

    def connects_to(self, compartment):
        if self.volume_element == compartment.volume_element:
            return True  # We're in the same "space"!

        elif self.volume_element.interface_with(compartment.volume_element) > 0:
            return True  # Our "spaces" touch!

        elif compartment in self.custom_linked_compartments:
            return True

        # To bad, we just didn't connect
        return False

    def is_next_to(self, compartment):
        if self.volume_element == compartment.volume_element:
            return False  # We're actually in the same "space" ...

        if self.volume_element.interface_with(compartment.volume_element) > 0:
            return True  # Our "spaces" touch!

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


@register_serializer(Compartment)
def serialize_compartment(comp: Compartment):
    s = {
        'id': comp.id,
        'name': comp.name
    }
    return s


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
        backref=sa.orm.backref('_links')
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
