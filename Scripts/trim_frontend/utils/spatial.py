import json
import re

from shapely.geometry import Polygon, Point, MultiPoint
from shapely.ops import nearest_points
import utm


# function to look up coordinates of a point from pre-defined df_points DataFrame.
# support function for Polygon_area function
def look_up_coords(df_points, point_name):
    x = float(df_points['x'].loc[df_points['point_id'] == point_name].values[0])
    y = float(df_points['y'].loc[df_points['point_id'] == point_name].values[0])
    return x, y


# function to make shapely polygon objects of all parcels
def make_polygons(df_parcels, df_points):
    pids = zip(df_parcels['point_ids'], df_parcels['parcel_name'])
    dict_polys = {}  # list of Polygon objects
    for pid, parcel_name in pids:  # loop over parcels
        points = pid.split(' ')  # get parcel points
        poly_coords = []  # list of x,y tuples
        for point in points:  # loop over points in parcel
            x_y_coords = look_up_coords(df_points, point)  # get x,y
            poly_coords.append(x_y_coords)  # add to parcel list
        dict_polys[parcel_name] = Polygon(poly_coords)  # make a Polygon and append it
    return dict_polys


# function to make list of shapely point objects of all points in the aermod file
def make_points(df_aermod):
    points_coords = zip(df_aermod.X,df_aermod.Y)
    points_list = [Point(x, y) for x, y in points_coords]
    return points_list


# to determine distance of a point from its nearest neighbor in the aermod file
def determine_nearest_neighbor_distance(point_x, point_y, df_aermod):
    points_list = make_points(df_aermod)  # make a  list of shapely points for each aermod receptor
    point = Point(point_x, point_y)  # make a shapely point object of current point of interest
    # list of shapely point objects of all receptors excluding current receptor
    all_other_points = [p for p in points_list if (p.x != point_x or p.y != point_y)]
    all_other_points = MultiPoint(all_other_points)  # multipoint object
    # returns tuple of origin and destination points -- we want the destination (other point)
    nearest_point = nearest_points(point, all_other_points)
    dist = point.distance(nearest_point[1])  # distance of point of interest to nearest neighbor
    return dist


# to determine which polygon a point lies in
def determine_location(dict_poly, x, y):
    test_point = Point(x, y)
    for k, v in dict_poly.items():
        if v.contains(test_point):
            return k
    return ""


# accepts number+letter like "30F", "14t", etc.
# returns a tuple with "is it valid" as first element and cleaned name as second
# case- / whitespace- insensitive
def is_utm_zone_valid(utm_zone):
    cleaned = utm_zone.strip().upper().replace(" ", "")
    pattern = r"^([1-9]|[1-5][0-9]|60)([A-HJ-NP-Z])$"
    is_valid = re.match(pattern, cleaned) is not None
    return (is_valid, cleaned if is_valid else None)


# TODO - let's define things like UTM, WGS84_LONGLAT, etc. someplace else...
def translate_position(x, y, from_system, to_system, **kwargs):
    utm_zone = None
    if from_system == "UTM" or to_system == "UTM":
        utm_zone = kwargs.get("utm_zone")

    if from_system == "UTM":
        if to_system == "WGS84_LONGLAT":
            converted = utm.to_latlon(x, y, int(utm_zone[0:-1]), utm_zone[-1])
            return [converted[1], converted[0]]
        else:
            raise Exception("Unsupported translation request from '{from_system}' to '{to_system}'")
    elif from_system == "WGS84_LONGLAT":
        if to_system == "UTM":
            converted = utm.from_latlon(y, x)
            return [converted[0], converted[1], f"{converted[2]}{converted[3]}"]
        else:
            raise Exception("Unsupported translation request from '{from_system}' to '{to_system}'")
    else:
        raise Exception("Unsupported translation request from '{from_system}'")


def translate_coordinates(polygon_definition, from_system, to_system, **kwargs):
    if from_system == to_system:
        return polygon_definition

    default_utm_zone = None
    if from_system == "UTM" or to_system == "UTM":
        default_utm_zone = kwargs.get("default_utm_zone")

    translated = []
    for vertex in polygon_definition:
        x = float(vertex[0])
        y = float(vertex[1])
        override = vertex[2] if len(vertex) > 2 else None

        translate_params = {}
        if from_system == "UTM" or to_system == "UTM":
            translate_params["utm_zone"] = override or default_utm_zone

        translated_xy = translate_position(x, y, from_system, to_system, **translate_params)
        translated.append(translated_xy)

    return translated


# given list of x/y (+utm maybe?) points, ensure that the polygon closes
def ensure_closed_polygon(polygon_definition):
    if len(polygon_definition) >= 3:
        first_point = json.dumps(polygon_definition[0])
        last_point = json.dumps(polygon_definition[-1])

        if first_point != last_point:
            copied_point = [polygon_definition[0][0], polygon_definition[0][1]]
            if len(polygon_definition[0]) == 3:
                copied_point.append(polygon_definition[0][2])
            polygon_definition.append(copied_point)

            return polygon_definition
        else:
            return polygon_definition
    else:
        return polygon_definition
