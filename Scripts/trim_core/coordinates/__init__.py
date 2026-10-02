import json
import utm


class CoordinateMapper:
    @classmethod
    def is_valid_utm_zone(cls, zone_name: str, use_mgrs: bool = False) -> bool:
        try:
            cls.decompose_utm_zone(zone_name, use_mgrs=use_mgrs)
            return True
        except Exception:
            return False

    @classmethod
    def decompose_utm_zone(cls, zone_name: str, use_mgrs=False) -> tuple[int, str | None]:
        """
        - All UTM codes are case/whitespace insensitive.
        - For UTM + hemisphere designators: Valid zones are 1N-60N, 1S-60S.
        - For UTM + MGRS: Valid zones are 1C-60Y with no A/B/I/O/Y/Z.
        """
        if not zone_name:
            raise ValueError(f'Invalid UTM Zone: "{zone_name}"')
        cleaned = ''.join(str(zone_name).split()).upper()

        zone_number = None
        zone_letter = None

        if len(cleaned) >= 2:
            if cleaned[-1].isalpha():
                zone_letter = cleaned[-1]
                zone_number = cleaned[:-1]
            else:
                zone_number = cleaned

        if (zone_letter is not None):
            if (use_mgrs and zone_letter in 'ABIOYZ') or (not use_mgrs and zone_letter not in 'NS'):
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

    def __init__(
        self,
        from_system: str,
        to_system: str,
        *,
        utm_zone: str | None = None,
        use_mgrs: bool = False
    ):
        from_system = from_system.upper()
        if from_system not in CoordinateMapper._COORDINATE_MAPPINGS:
            raise ValueError(f"Unsupported translation request from '{from_system}'")
        self._from = from_system

        to_system = to_system.upper()
        if to_system not in CoordinateMapper._COORDINATE_MAPPINGS[from_system]:
            raise ValueError(
                f"Unsupported translation request from '{from_system}' to '{to_system}'"
            )
        self._to = to_system

        self._use_mgrs = use_mgrs

        self._utm_zone = None
        if 'UTM' in from_system:
            if utm_zone is None:
                raise ValueError(
                    f"Unsupported translation request: '{from_system}' requires `utm_zone` to be specified"
                )
            self._utm_zone = CoordinateMapper.decompose_utm_zone(
                utm_zone, self._use_mgrs
            )

    @property
    def _utm_zone_number(self) -> int | None:
        if not self._utm_zone:
            return None
        return self._utm_zone[0]

    @property
    def _utm_zone_letter(self) -> str | None:
        if not self._utm_zone:
            return None
        return self._utm_zone[1]

    def translate(self, x: float, y: float):
        converted = CoordinateMapper._COORDINATE_MAPPINGS[self._from][self._to](
            x, y,
            zone_number=self._utm_zone_number,
            zone_letter=self._utm_zone_letter
        )
        return CoordinateMapper._RETURN_FORMAT[self._to](converted)


# given list of x/y (+utm maybe?) points, ensure that the polygon closes
def ensure_closed_polygon(points: list[list]):
    if len(points) >= 3:
        first_point = json.dumps(points[0])
        last_point = json.dumps(points[-1])
        if first_point != last_point:
            points.append(list(points[0]))
            return points
        else:
            return points
    else:
        return points
