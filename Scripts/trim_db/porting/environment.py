import os
from .config import *
from .utils import *
from ..services import *


__all__ = [
    'parse_volume_elements',
    'parse_compartments',
    'clean_compartment_name',
    'create_compartment'
]


def clean_compartment_name(name):
    name = name.replace('/', '_')
    name = name.replace(' - ', '_').replace(' ', '_')
    return name


def parse_volume_elements(scenario, vol_file):
    print(
        'Parsing volume elements'
        f' from "{os.path.basename(vol_file)}" ...'
    )

    with open(vol_file, 'r') as f:
        lines = f.readlines()

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
        # PointName: [x, y]
        line.split()[0]: [float(line.split()[1]), float(line.split()[2])]
        for line in parsed_lines['points']
    }

    for line in parsed_lines['parcels']:
        line = line.split()
        p = ParcelService.get_or_create(
            name=line[0], scenario_id=scenario.id,
            no_commit=True
        )
        vertices_coord = transform_coordinates_to_decimal([points[pid] for pid in line[2:]])
        # p.vertices = [points[pid] for pid in line[2:]]
        p.vertices = vertices_coord
        ParcelService.commit()

    for line in parsed_lines['volume_elements']:
        # Split on " to create list of size 3;
        # the middle element is the primary abiotic name
        line = [x.strip() for x in line.split('"')]

        name = line[0].split()
        primary_abiotic = line[1]
        coords = line[2].split()

        p_name = name[1]
        v_name = name[0]
        if v_name.endswith(f'_{p_name}'):
            v_name = v_name[:-len(f'_{p_name}')]

        v = VolumeElementService.get_or_create(
            name=v_name,
            parcel_id=ParcelService.get(name=p_name).id,
            bottom=float(coords[0]),
            top=float(coords[1])
        )

        create_compartment(primary_abiotic, v, no_commit=True)

    VolumeElementService.commit()


def create_compartment(name, volume_element=None, no_commit=False):
    name = clean_compartment_name(name)

    m_name = MEDIA_MAP.get(name, name)

    m = CompartmentService.media.get_or_create(category=m_name)

    c = CompartmentService.get_or_create(
        name=name,
        media_id=m.id,
        volume_element_id=None if not volume_element else volume_element.id,
        no_commit=True
    )
    if volume_element is not None:
        c.volume_element = volume_element
        if not no_commit:
            CompartmentService.commit()
    return c


def parse_compartments(scenario, comp_file):
    print(
        f'Parsing compartments from "{os.path.basename(comp_file)}" ...'
    )

    with open(comp_file, 'r') as f:
        lines = f.readlines()

    ve = None
    for line in lines:
        line = line.split('//')[0].strip()  # remove comment
        if not line:
            continue  # Nothing to see here

        line = line.split(':')
        if line[0] == 'VolumeElement':
            ve_name = line[1].strip()
            ve = scenario.get_volume_element(ve_name)
            if not ve:
                print(ve_name)
                raise AssertionError

        if line[0] == 'Compartment':
            c_name = line[1].strip()
            if ve is None:
                print(c_name)
                raise AssertionError
            create_compartment(c_name, ve, no_commit=True)

    CompartmentService.commit()

