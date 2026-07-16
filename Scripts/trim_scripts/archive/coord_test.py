from pyproj import CRS, Transformer
import json
from shapely.geometry import Point, Polygon
from trim_db.schema.parameters.utils import ureg
import utm


class UtmTransformer:
    # Initializes default UTM Transformer settings
    # so we don't have to do this every time we need a transformer
    from_crs = CRS.from_epsg(4326)
    to_crs = CRS.from_wkt(  # CAREFUL: we assume ellipsoid is WGS84 ..
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
    transformer = Transformer.from_crs(from_crs, to_crs)

    @classmethod
    def transform(cls, *args, **kwargs):
        return cls.transformer.transform(*args, **kwargs)


class Parcel():
    _vertices = []
    _utm_vertices = None
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
        self._utm_vertices = None
        self._utm_polygon = None
        self._polygon = None
        self._area = None

    def __init__(self, verts):
        self.vertices = verts

    @property
    def utm_vertices(self):
        return [
            wgs_utm_mapper.translate(*pt) for pt in self.vertices
        ]

    @property
    def alt_utm_vertices(self):
        utm_vert = [UtmTransformer.transform(pt[1], pt[0]) for pt in self.vertices]
        return utm_vert

    def polygon(self, utm=True):
        if utm:
            if self._utm_polygon is None:
                utm_zone = set([pt[-1] for pt in self.utm_vertices])
                if len(utm_zone) > 1:
                    raise ValueError(f'Parcel spans multiple UTM zones ({", ".join(utm_zone)}); no valid UTM polygon can be constructed.')
                self._utm_polygon = Polygon([pt[:2] for pt in self.utm_vertices])
            return self._utm_polygon
        if self._polygon is None:
            self._polygon = Polygon(self.vertices)
        return self._polygon

    def alt_polygon(self, utm=True):
        return Polygon([pt[:2] for pt in self.alt_utm_vertices])

    def contains_point(self, *args, utm=True):
        if len(args) > 1:
            return self.polygon(utm).contains(Point(*args))
        return self.polygon(utm).contains(Point(args))

    def alt_contains_point(self, *args, utm=True):
        if len(args) > 1:
            return self.alt_polygon(utm).contains(Point(*args))
        return self.alt_polygon(utm).contains(Point(args))

    @property
    def area(self):
        # CAREFUL: we assume dimensions are in meters ...
        if self._area is None:
            self._area = self.polygon().area * ureg('m^2')
        return self._area


class CoordinateMapper:
    @classmethod
    def is_valid_utm_zone(cls, zone_name):
        """
        Valid zones are 1A-60Z with no I/O. Case/whitespace insensitive.
        """
        try:
            cls.decompose_utm_zone(zone_name)
            return True
        except Exception:
            return False

    @classmethod
    def decompose_utm_zone(cls, zone_name):
        """
        Valid zones are 1A-60Z with no I/O. Case/whitespace insensitive.
        """
        if not zone_name:
            raise ValueError(f'Invalid UTM Zone: "{zone_name}"')
        cleaned = ''.join(zone_name.split()).upper()
        try:
            zone_letter = cleaned[-1]
            zone_number = cleaned[:-1]
        except IndexError:
            raise ValueError(f'Invalid UTM Zone: "{cleaned}"')
        
        if (not zone_letter.isalpha()) or (zone_letter in 'IO'):
            raise ValueError(f'Invalid UTM Zone Letter: "{zone_letter}"')

        try:
            zone_number = int(zone_number)
        except (TypeError, ValueError):
            raise ValueError(f'Invalid UTM Zone Number: "{zone_number}"')
        if zone_number < 1 or zone_number > 60:
            raise ValueError(f'Invalid UTM Zone Number: "{zone_number}"')
        
        return (zone_number, zone_letter)

    _COORDINATE_MAPPINGS = {
        'UTM': {
            'WGS84_LONGLAT': lambda x, y, **kwargs: utm.to_latlon(x, y, kwargs['zone_number'], kwargs['zone_letter'])
        },
        'WGS84_LONGLAT': {
            'UTM': lambda x, y, **kwargs: utm.from_latlon(y, x)
        }
    }
    _RETURN_FORMAT = {
        'WGS84_LONGLAT': lambda coords: (coords[1], coords[0]),
        'UTM': lambda coords: (coords[0], coords[1], f"{coords[2]}{coords[3]}")
    }

    def __init__(self, from_system, to_system, **kwargs):
        from_system = from_system.upper()
        if from_system not in CoordinateMapper._COORDINATE_MAPPINGS:
            raise ValueError(f"Unsupported translation request from '{from_system}'")
        self._from = from_system

        to_system = to_system.upper()
        if to_system not in CoordinateMapper._COORDINATE_MAPPINGS[from_system]:
            raise ValueError(f"Unsupported translation request from '{from_system}' to '{to_system}'")
        self._to = to_system

        self._utm_zone = None
        if 'UTM' in from_system:
            self._utm_zone = CoordinateMapper.decompose_utm_zone(kwargs.get("utm_zone"))

    @property
    def _utm_zone_number(self):
        if not self._utm_zone:
            return None
        return self._utm_zone[0]

    @property
    def _utm_zone_letter(self):
        if not self._utm_zone:
            return None
        return self._utm_zone[1]

    def translate(self, x, y):
        converted = CoordinateMapper._COORDINATE_MAPPINGS[self._from][self._to](
            x, y,
            zone_number=self._utm_zone_number,
            zone_letter=self._utm_zone_letter
        )
        return CoordinateMapper._RETURN_FORMAT[self._to](converted)


wgs_utm_mapper = CoordinateMapper('WGS84_LONGLAT', 'UTM')


def test():
    from pyproj import Geod

    print('\n=======================================================\n')

    verts = [
        [-85.33404253646208, 44.22647738643362],
        [-85.36564449106953, 44.24230857894454],
        [-85.33610064064906, 44.26507056695825],
        [-85.33404253646208, 44.22647738643362]
    ]
    pcl = Parcel(verts)
    print('pcl lonlat =', pretty_print_verts(pcl.vertices))
    # print('area =', (pcl.polygon(utm=False).area * ureg('deg^2')))
    print('')
    print('old utm =', pretty_print_verts(pcl.alt_utm_vertices))
    print('old (fixed-zone) utm area =', pcl.alt_polygon(utm=True).area * ureg('m^2'))
    print('')
    print('new utm =', pretty_print_verts(pcl.utm_vertices))
    print(set([pt[-1] for pt in pcl.utm_vertices]))
    try:
        print('new (zone-aware) utm area =', pcl.polygon(utm=True).area * ureg('m^2'))
    except Exception as e:
        print(e)
    print('')
    print('geod area =', abs(Geod(ellps='WGS84').geometry_area_perimeter(pcl.polygon(utm=False))[0]))

    print('\n----------------------\n')

    pt = [-85.34, 44.25]
    print('test point lonlat =', pt)
    alt_utm_pt = UtmTransformer.transform(pt[1], pt[0])
    print('test point utm (old) =', alt_utm_pt)
    utm_pt = wgs_utm_mapper.translate(*pt)
    print('test point utm (new) =', utm_pt)
    print('')
    print('pcl contains point (lonlat) =', pcl.contains_point(pt, utm=False))
    print('pcl contains point (old utm) =', pcl.alt_contains_point(alt_utm_pt[:2], utm=True))
    try:
        print('pcl contains point (new utm) =', pcl.contains_point(utm_pt[:2], utm=True))
    except Exception as e:
        print(e)

    print('\n=======================================================\n')

    verts = [
        [-77.9, 35.4],
        [-78.1, 35.4],
        [-78.1, 35.8],
        [-77.8, 35.75]
    ]
    pcl = Parcel(verts)
    print('pcl lonlat =', pretty_print_verts(pcl.vertices))
    # print('area =', (pcl.polygon(utm=False).area * ureg('deg^2')))
    print('')
    print('old utm =', pretty_print_verts(pcl.alt_utm_vertices))
    print('old (fixed-zone) utm area =', pcl.alt_polygon(utm=True).area * ureg('m^2'))
    print('')
    print('new utm =', pretty_print_verts(pcl.utm_vertices))
    print(set([pt[-1] for pt in pcl.utm_vertices]))
    try:
        print('new (zone-aware) utm area =', pcl.polygon(utm=True).area * ureg('m^2'))
    except Exception as e:
        print(e)
    print('')
    print('geod area =', abs(Geod(ellps='WGS84').geometry_area_perimeter(pcl.polygon(utm=False))[0]))

    print('\n----------------------\n')

    pt = [-77.95, 35.6]
    # pt = [-78.0996, 35.39504]
    print('test point lonlat =', pt)
    alt_utm_pt = UtmTransformer.transform(pt[1], pt[0])
    print('test point utm (old) =', alt_utm_pt)
    utm_pt = wgs_utm_mapper.translate(*pt)
    print('test point utm (new) =', utm_pt)
    print('')
    print('pcl contains point (lonlat) =', pcl.contains_point(pt, utm=False))
    print('pcl contains point (old utm) =', pcl.alt_contains_point(alt_utm_pt[:2], utm=True))
    try:
        print('pcl contains point (new utm) =', pcl.contains_point(utm_pt[:2], utm=True))
    except Exception as e:
        print(e)

    print('\n----------------------\n')

    upt = [236629, 3921297, '18S']
    utm_wgs_mapper = CoordinateMapper('UTM', 'WGS84_LONGLAT', utm_zone=upt[2])

    print('test utm point =', upt)
    print('pcl contains utm point (old utm) =', pcl.alt_contains_point(upt[:2], utm=True))
    try:
        print('pcl contains utm point (new utm) =', pcl.contains_point(upt[:2], utm=True))
    except Exception as e:
        print(e)
    lonlat_upt = utm_wgs_mapper.translate(*upt[:2])
    print('test utm point lonlat =', lonlat_upt)
    print('pcl contains utm point (lonlat) =', pcl.contains_point(lonlat_upt, utm=False))

    print('\n=======================================================\n')


def pretty_print_verts(verts):
    s = '['
    for v in verts:
        s += f'\n\t{v},'
    if len(s) > 1:
        s = s[:-1]
    s += '\n]'
    return s


if __name__ == '__main__': 
    test()
