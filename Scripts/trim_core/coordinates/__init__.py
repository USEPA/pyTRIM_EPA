import utm


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
