from shapely.geometry import Polygon, Point, MultiPoint
from shapely.ops import nearest_points


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
