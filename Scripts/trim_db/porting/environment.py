from ..schema.environment.models import *

__all__ = ['parse_volume_elements']


def parse_volume_elements(scenario_id, volume_elements_file):
    with open(volume_elements_file, 'r') as f:
        lines = f.readlines()

    def is_valid(line):
        # not a comment and not a blank
        return line[:2] != '//' and line != ''

    elements = ['points', 'parcels', 'volume_elements']

    parsed_lines = {x: [] for x in elements}
    copying = {}
    for line in lines:
        line = line.split('//')[0].strip()  # remove comment
        if not line:
            continue  # Nothing to see here

        for el in elements:
            if line == f'start_{el}':
                copying[el] = True
            elif line == f'end_{el}':
                copying.pop(el, False)
            elif copying.get(el):
                parsed_lines[el].append(line)

    points = {
        # PointName: (x, y)
        line.split()[0]: (float(line.split()[1]), float(line.split()[2]))
        for line in parsed_lines['points']
    }

    parcels = {
        line.split()[0]: {
            'point_ids': line.split()[2:]
        }
    }
    parcels = {}
    for line in parsed_lines['parcels']:
        line = line.split()
        p = Parcel(name=line[0], scenario_id=scenario_id)
        p.vertices = [points[pid] for pid in line[2:]]
        parcels[p.name] = p

    volume_elements = []
    for line in parsed_lines['volume_elements']:
        # Split on " to create list of size 3;
        # the middle element is the primary abiotic name
        line = [x.strip() for x in line.split('"')]

        name = line[0].split()
        primary_abiotic = line[1]
        coords = line[2].split()

        v = VolumeElement(
            name=name[0],
            parcel=parcels[name[1]],
            bottom=float(coords[0]),
            top=float(coords[1])
        )
        volume_elements.append(v)

    # Add models to db
    # TODO

    return volume_elements
