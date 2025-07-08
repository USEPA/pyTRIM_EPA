import time
import json
import math
import requests
import os
import numpy as np
import pandas as pd
from qgis import processing
from qgis.core import *
from shapely.geometry import shape
from Scripts.trim_frontend.external_API.helpers import convert_to_geojson
from trim_db.services import *

TEMP_PARCEL_NAME_COL = 'title'

### START: Samuel's USGS_API_TNM.py functions

def get_geojson_bbox(geojson_data):
    """
    Calculate the bounding box for all features in a GeoJSON
    Returns (minx, miny, maxx, maxy)
    """
    # Initialize with the first feature's bounds
    if not geojson_data['features']:
        raise ValueError("No features found in GeoJSON")
    
    first_geom = shape(geojson_data['features'][0]['geometry'])
    minx, miny, maxx, maxy = first_geom.bounds
    
    # Expand bounds to include all other features
    for feature in geojson_data['features'][1:]:
        geom = shape(feature['geometry'])
        feat_minx, feat_miny, feat_maxx, feat_maxy = geom.bounds
        
        minx = min(minx, feat_minx)
        miny = min(miny, feat_miny)
        maxx = max(maxx, feat_maxx)
        maxy = max(maxy, feat_maxy)
    
    return (minx, miny, maxx, maxy)

def download_elevation_data(bbox, output_path="elevation.tif"):
    """
    Download elevation data from USGS TNM API for the given bbox
    bbox should be (minx, miny, maxx, maxy)
    """
    # TNM API endpoint for elevation products
    tnm_api_url = "https://tnmaccess.nationalmap.gov/api/v1/products"
    
    # Parameters for the API request
    params = {
        'bbox': f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}",
        'datasets': 'National Elevation Dataset (NED) 1/3 arc-second',
        'prodFormats': 'GeoTIFF',
        'outputFormat': 'JSON'
    }
    
    print(f"Requesting elevation data for bbox: {params['bbox']}")
    
    # Make the API request
    response = requests.get(tnm_api_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    
    data = response.json()
    
    # Check if we got any results
    if not data.get('items'):
        raise Exception("No elevation data found for the specified area")
    
    # Get the download URL for the first item
    download_url = data['items'][0]['downloadURL']
    
    # Download the elevation data
    print(f"Downloading elevation data from {download_url}")
    response = requests.get(download_url, stream=True)
    
    if response.status_code != 200:
        raise Exception(f"Download failed with status code {response.status_code}")

    def convert_bytes(num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0

    # Save the file
    with open(output_path, 'wb') as f:
        looper = 0
        then = None
        for chunk in response.iter_content(chunk_size=8192):
            looper += 1
            if looper % 1000 == 0:
                curr_file_info = os.stat(output_path)
                curr_size = convert_bytes(curr_file_info.st_size)
                now = time.perf_counter_ns()
                if then is not None:
                    difference = f"{now - then}ns"
                else:
                    difference = "initial"
                print(f"[{difference}] streaming response iteration {looper}; {output_path} now {curr_size}...")
                then = now
            f.write(chunk)
    
    print(f"Elevation data saved to {output_path}")
    return output_path

### END: Samuel's USGS_API_TNM.py functions

### START: Samuel's GetFlow_V10 utility functions
# (copied 99% as-is from GetFlow_V10, the April 2025 version)
#   commented out sankey save to json
#   replaced parcel_name_col --> TEMP_PARCEL_NAME_COL
#   get_parcel_boundaries did not exist in v10 but still referenced
def get_parcel_boundaries(parcels_layer):
    """Get boundaries between parcels"""
    boundaries = []
    for feature1 in parcels_layer.getFeatures():
        geom1 = feature1.geometry()
        title1 = feature1[TEMP_PARCEL_NAME_COL]
        
        # Find neighboring parcels
        for feature2 in parcels_layer.getFeatures():
            if feature1.id() >= feature2.id():
                continue
                
            geom2 = feature2.geometry()
            title2 = feature2[TEMP_PARCEL_NAME_COL]
            
            if geom1.touches(geom2):
                shared_boundary = geom1.intersection(geom2)
                if shared_boundary.length() > 0:
                    boundaries.append({
                        'parcel1': title1,
                        'parcel2': title2,
                        'boundary': shared_boundary
                    })
    
    return boundaries

def get_exterior_boundary(geom):
    """Extract the exterior boundary as a line geometry from a polygon geometry."""
    if geom.isMultipart():
        multi_poly = geom.asMultiPolygon()
        if multi_poly and len(multi_poly) > 0 and len(multi_poly[0]) > 0:
            ring = multi_poly[0][0]
            return QgsGeometry.fromPolylineXY(ring)
    else:
        poly = geom.asPolygon()
        if poly and len(poly) > 0:
            ring = poly[0]
            return QgsGeometry.fromPolylineXY(ring)
    return None

def get_external_boundaries(parcels_layer):
    """Get boundaries between parcels and the outside world (sink)"""
    external_boundaries = []
    
    dissolve_params = {
        'INPUT': parcels_layer.source(),  # Use the source path instead of the layer object
        'FIELD': [],  # No field for dissolving - dissolve all
        'OUTPUT': 'memory:'
    }
    dissolved_result = processing.run("native:dissolve", dissolve_params)
    dissolved_layer = dissolved_result['OUTPUT']
    
    if dissolved_layer.featureCount() > 0:
        dissolved_feature = next(dissolved_layer.getFeatures())
        dissolved_geom = dissolved_feature.geometry()
        exterior_boundary = get_exterior_boundary(dissolved_geom)
        
        if exterior_boundary is not None:
            for feature in parcels_layer.getFeatures():
                geom = feature.geometry()
                title = feature[TEMP_PARCEL_NAME_COL]
                parcel_boundary = get_exterior_boundary(geom)
                if parcel_boundary is None:
                    continue
                external_intersection = parcel_boundary.intersection(exterior_boundary)
                if not external_intersection.isEmpty() and external_intersection.length() > 0:
                    external_boundaries.append({
                        'parcel': title,
                        'boundary': external_intersection
                    })
    return external_boundaries

def get_points_along_line(line_geom, interval):
    """Sample points along a line geometry at regular intervals"""
    points = []
    if line_geom.isMultipart():
        for part in line_geom.asGeometryCollection():
            if part.type() == QgsWkbTypes.LineGeometry:
                length = part.length()
                current_distance = 0
                while current_distance <= length:
                    point = part.interpolate(current_distance)
                    points.append(point.asPoint())
                    current_distance += interval
    else:
        length = line_geom.length()
        current_distance = 0
        while current_distance <= length:
            point = line_geom.interpolate(current_distance)
            points.append(point.asPoint())
            current_distance += interval
    return points

def get_flow_vector(direction):
    """Convert GRASS flow direction (1-8) to vector"""
    directions = {
        1: (1, 0),     # East
        2: (1, 1),     # Southeast
        3: (0, 1),     # South
        4: (-1, 1),    # Southwest
        5: (-1, 0),    # West
        6: (-1, -1),   # Northwest
        7: (0, -1),    # North
        8: (1, -1)     # Northeast
    }
    return directions.get(int(direction) if direction is not None else 0, (0, 0))

def get_boundary_vector_for_point(point, boundary_geom):
    """Get normalized boundary vector at a specific point"""
    min_distance = float('inf')
    best_vector = (0, 0)
    if boundary_geom.isMultipart():
        geometries = boundary_geom.asGeometryCollection()
    else:
        geometries = [boundary_geom]
    for geom in geometries:
        if geom.type() == QgsWkbTypes.LineGeometry:
            vertices = geom.asPolyline()
            for i in range(len(vertices) - 1):
                start = vertices[i]
                end = vertices[i + 1]
                segment_point = closest_point_on_segment(point, start, end)
                distance = point.distance(segment_point)
                if distance < min_distance:
                    min_distance = distance
                    dx = end.x() - start.x()
                    dy = end.y() - start.y()
                    length = (dx**2 + dy**2)**0.5
                    if length > 0:
                        best_vector = (dx/length, dy/length)
    return best_vector

def closest_point_on_segment(point, start, end):
    """Find the closest point on a line segment to a given point"""
    px = point.x()
    py = point.y()
    x1 = start.x()
    y1 = start.y()
    x2 = end.x()
    y2 = end.y()
    line_length_squared = (x2 - x1)**2 + (y2 - y1)**2
    if line_length_squared == 0:
        return start
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / line_length_squared))
    return QgsPointXY(x1 + t * (x2 - x1), y1 + t * (y2 - y1))

def vector_dot_product(v1, v2):
    """Calculate dot product of two vectors"""
    return v1[0]*v2[0] + v1[1]*v2[1]

def get_boundary_normal_vector(point, boundary_geom, parcels_layer):
    """Get normal vector pointing inward from boundary at point"""
    boundary_vector = get_boundary_vector_for_point(point, boundary_geom)
    normal1 = (-boundary_vector[1], boundary_vector[0])
    normal2 = (boundary_vector[1], -boundary_vector[0])
    buffer_distance = 0.0001
    for feature in parcels_layer.getFeatures():
        geom = feature.geometry()
        test_point1 = QgsGeometry.fromPointXY(QgsPointXY(
            point.x() + normal1[0] * buffer_distance, 
            point.y() + normal1[1] * buffer_distance))
        test_point2 = QgsGeometry.fromPointXY(QgsPointXY(
            point.x() + normal2[0] * buffer_distance, 
            point.y() + normal2[1] * buffer_distance))
        if geom.contains(test_point1):
            return normal1
        elif geom.contains(test_point2):
            return normal2
    return normal1

def analyze_flow_at_boundary(boundary, accum_layer, direction_layer):
    """Analyze flow across a specific boundary"""
    sample_interval = direction_layer.rasterUnitsPerPixelX()
    points = get_points_along_line(boundary['boundary'], sample_interval)
    flow_1_to_2 = 0
    flow_2_to_1 = 0
    for point in points:
        accum_value = accum_layer.dataProvider().identify(
            point, QgsRaster.IdentifyFormatValue).results().get(1)
        direction_value = direction_layer.dataProvider().identify(
            point, QgsRaster.IdentifyFormatValue).results().get(1)
        if accum_value is not None and direction_value is not None and accum_value > 0:
            flow_vector = get_flow_vector(direction_value)
            boundary_vector = get_boundary_vector_for_point(point, boundary['boundary'])
            dot_product = vector_dot_product(flow_vector, boundary_vector)
            if dot_product > 0:
                flow_1_to_2 += accum_value
            elif dot_product < 0:
                flow_2_to_1 += accum_value
    return flow_1_to_2, flow_2_to_1

def analyze_sink_flows(parcels_layer, accum_layer, direction_layer):
    """
    Analyze flows to/from the sink (outside any parcel) using explicit external boundaries.
    """
    sink_flows = {}
    external_boundaries = get_external_boundaries(parcels_layer)
    cell_size = direction_layer.rasterUnitsPerPixelX()
    for ext_bound in external_boundaries:
        parcel_id = ext_bound['parcel']
        boundary_geom = ext_bound['boundary']
        points = get_points_along_line(boundary_geom, cell_size)
        outflow = 0
        inflow = 0
        for point in points:
            accum_value = accum_layer.dataProvider().identify(
                point, QgsRaster.IdentifyFormatValue).results().get(1)
            direction_value = direction_layer.dataProvider().identify(
                point, QgsRaster.IdentifyFormatValue).results().get(1)
            if accum_value is None or direction_value is None or accum_value <= 0:
                continue
            normal = get_boundary_normal_vector(point, boundary_geom, parcels_layer)
            flow_vector = get_flow_vector(direction_value)
            dot_product = vector_dot_product(flow_vector, normal)
            if dot_product > 0:
                outflow += accum_value
            elif dot_product < 0:
                inflow += accum_value
        sink_flows[parcel_id + "_to_sink"] = outflow
        sink_flows[parcel_id + "_from_sink"] = inflow
    return sink_flows

def create_flow_matrix_with_sink(parcels_layer, accum_layer, direction_layer):
    """Create flow matrix between all parcels including sink (outside any parcel)"""
    titles = [f[TEMP_PARCEL_NAME_COL] for f in parcels_layer.getFeatures()]
    all_titles = titles + ["SINK"]
    flow_matrix = pd.DataFrame(0, index=all_titles, columns=all_titles)
    boundaries = get_parcel_boundaries(parcels_layer)
    for boundary in boundaries:
        flow_1_to_2, flow_2_to_1 = analyze_flow_at_boundary(
            boundary, accum_layer, direction_layer)
        flow_matrix.loc[boundary['parcel1'], boundary['parcel2']] = flow_1_to_2
        flow_matrix.loc[boundary['parcel2'], boundary['parcel1']] = flow_2_to_1
    sink_flows = analyze_sink_flows(parcels_layer, accum_layer, direction_layer)
    for key, flow in sink_flows.items():
        if "_to_sink" in key:
            parcel = key.replace("_to_sink", "")
            flow_matrix.loc[parcel, "SINK"] = flow
        elif "_from_sink" in key:
            parcel = key.replace("_from_sink", "")
            flow_matrix.loc["SINK", parcel] = flow
    flow_matrix.loc["TOTAL_OUT", :] = flow_matrix.sum(axis=0)
    flow_matrix.loc[:, "TOTAL_IN"] = flow_matrix.sum(axis=1)
    return flow_matrix

def create_sankey_data(flow_matrix):
    """Create simplified data for Sankey diagram visualization"""
    sankey_data = []
    for source in flow_matrix.index:
        if source in ["TOTAL_OUT", "TOTAL_IN"]:
            continue
        for target in flow_matrix.columns:
            if target in ["TOTAL_OUT", "TOTAL_IN"]:
                continue
            flow = flow_matrix.loc[source, target]
            if flow > 0:
                sankey_data.append({
                    "source": source,
                    "target": target,
                    "value": float(flow)
                })
    #import json
    #with open(CURRENT_FOLDER_PATH + '/flow_sankey_data.json', 'w') as f:
    #    json.dump(sankey_data, f)
    return sankey_data

### END: Samuel's GetFlow_V10 utility functions

def run_getflow_v10_for_scenario_id(scenario_id):
    print(f"v7 entrypoint for '{scenario_id}', alternate construction approach...")
    # parcels_for_this_scenario = json.dumps(ParcelService.get_all(scenario_id=scenario_id))

    print(f"build ntov (expect 35, -78, NOT -78,35")
    names_to_vertices = {}
    parcels = ParcelService.get_all(scenario_id=scenario_id)
    for p in parcels:
        # names_to_vertices[p.name] = p.vertices
        names_to_vertices[p.name] = [(v[1], v[0]) for v in p.as_serializable()['vertices']]
    # print(f"convert it ({names_to_vertices})")
    # parcels_for_this_scenario = json.dumps(names_to_vertices)
    print(f"KEEP AS IS!")
    parcels_for_this_scenario = names_to_vertices


    print(f"LOADED PARCELS: {parcels_for_this_scenario}")
    print(f"RUNNING FOR REALSKI!")
    return run_getflow_v10(parcels_for_this_scenario)


def run_getflow_v10(parcels):
    # make it fast
    print(f"TIBSV7 RUN_GETFLOW_V10 FAKE ({type(parcels)}): {parcels}")
    sep = os.path.sep

    """
    print(f"{'*'*20}ALGORITHMS START{'*'*20}\n")
    print(f"{'display name':<60}{'name':<60}{'id':<45}")
    print("-" * 165)
    for alg in QgsApplication.processingRegistry().algorithms():
        stuff_to_find = [ "cliprasterbymasklayer", "saga", "grass7", "joinbylocation" ]
        do_print = False
        for s in stuff_to_find:
            if True or s in alg.id():
                do_print = True
                break

        if do_print:
            print(f"{alg.displayName():<60}{alg.name():<60}{alg.id():<45}")
    print(f"\n{'*'*20}ALGORITHMS END{'*'*20}")

    1/0
    """
    # import code; code.interact(local=locals())

    USE_PRECANNED_TEST_DATA = False

    # Paths to your data
    current_folder_path = os.path.realpath(os.path.dirname(__file__))
    print(f"TIBSV7 let's look in '{current_folder_path}'...")

    # qgis_project_file = current_folder_path + r"\GetFlow_2.qgs"  # Specify the correct project file path

    if USE_PRECANNED_TEST_DATA:
        # hardcoded temp test with good Samuel data
        parcel_layer = current_folder_path + "/Durham_Parcels.geojson"
        print(f"TIBSV7 using hardcoded parcels '{parcel_layer}'")

        dem_raster_layer = current_folder_path + f"{sep}USGS_1_n36w083_20220512.tif"
    else:
        # real conversion of passed-in parcels
        parcel_layer = convert_to_geojson.GeoJson(parcels).convert_json()
        print(f"TIBSV7 using real converted parcels '{parcel_layer}'")

        # 202502B: get bounding box of the dynamic layer
        with open(parcel_layer) as f:
            loaded_geojson_data = json.load(f)
            bbox = get_geojson_bbox(loaded_geojson_data)

        # Download the elevation data
        dem_raster_layer = current_folder_path + f"{sep}dynamic_elevation_data.tif"

        if True:
            try:
                # TODO -- can we somehow cache this? These files are *very* big. e.g. name them based on
                # bounding box and upload that to S3? Can we be smarter?
                dem_raster_layer = download_elevation_data(bbox, dem_raster_layer)
                print(f"Successfully downloaded elevation data to {dem_raster_layer}")
            except Exception as e:
                print(f"Error downloading elevation data: {str(e)}")
                raise e
        else:
            print(f"USING PRE-DOWNLOADED tif FILE FOR DEBUGGING SPEED ({dem_raster_layer})")
            print(f"(did you alter prepare_dockerized.py to copy it in?)")

    print(f"TIBSV7 PAST PARCEL/TIF SECTION ({USE_PRECANNED_TEST_DATA}): '{dem_raster_layer}' / '{parcel_layer}'")

    # TEMP_PARCEL_NAME_COL = 'title'
    print(f"TIBSV7 converted ({parcel_layer})")

    # Load parcels and DEM layers
    parcels = QgsVectorLayer(parcel_layer, "Parcels", "ogr")
    dem = QgsRasterLayer(dem_raster_layer, "DEM")

    # Add layers to the project
    QgsProject.instance().addMapLayer(parcels)
    QgsProject.instance().addMapLayer(dem)

    # ----------------------------------------------------------
    # STEP 1: Buffer the parcels to include edge pixels in the clip
    # ----------------------------------------------------------
    print(f"STEP 1: Buffer the parcels to include edge pixels in the clip")
    # Determine an appropriate buffer distance; one option is to use the cell size of your DEM.
    cell_size = dem.rasterUnitsPerPixelX()  # assuming square cells; adjust if necessary
    buffer_distance = cell_size * 20  # Adjust multiplier as needed

    buffer_params = {
        'INPUT': parcel_layer,
        'DISTANCE': buffer_distance,
        'SEGMENTS': 5,
        'DISSOLVE': True,
        'OUTPUT': 'memory:'
    }
    buffer_result = processing.run("native:buffer", buffer_params)
    buffered_parcels = buffer_result['OUTPUT']  # Use the layer directly
    QgsProject.instance().addMapLayer(buffered_parcels)


    # ----------------------------------------------------------
    # STEP 2: Clip the DEM using the buffered parcel layer
    # ----------------------------------------------------------
    print(f"STEP 2: Clip the DEM using the buffered parcel layer")
    clip_params = {
        'INPUT': dem_raster_layer,
        'MASK': buffered_parcels,  # using buffered parcels instead of original parcels
        'SOURCE_CRS': None,
        'TARGET_CRS': None,
        'TARGET_EXTENT': None,
        'NODATA': None,
        'ALPHA_BAND': False,
        'CROP_TO_CUTLINE': True,
        'KEEP_RESOLUTION': False,
        'SET_RESOLUTION': False,
        'X_RESOLUTION': None,
        'Y_RESOLUTION': None,
        'MULTITHREADING': False,
        'OPTIONS': '',
        'DATA_TYPE': 0,
        'EXTRA': '',
        'OUTPUT': 'TEMPORARY_OUTPUT'
    }

    result = processing.run("gdal:cliprasterbymasklayer", clip_params)
    ClippedRaster = QgsRasterLayer(result['OUTPUT'], "ClippedRaster")
    QgsProject.instance().addMapLayer(ClippedRaster)


    # TEST START - dump out QgsRasterLayer
    print(f"raster width: {ClippedRaster.width()}")

    def dump_raster_layer_to_file(rl, filename, coord_system = "EPSG:4326"):
        if (type(rl) is str):
            import sys
            print(f"whoops, did you pass in the path and not the actual RasterLayer?")
            sys.exit(1)

        pipe = QgsRasterPipe()
        pipe.set(rl.dataProvider().clone())
        file_writer = QgsRasterFileWriter(filename)
        file_writer.writeRaster(pipe, rl.width(),rl.height(), rl.extent(), QgsCoordinateReferenceSystem(coord_system))
        print(f"wrote file to '{filename}'")

    dump_raster_layer_to_file(dem, "/app/pytrim_getflow_src/demDebug.tif")
    dump_raster_layer_to_file(ClippedRaster, "/app/pytrim_getflow_src/ClippedRasterDebug.tif")
    # TEST END - dump out QgsRasterLayer


    # ----------------------------------------------------------
    # STEP 3: Continue with filling depressions and watershed analysis
    # ----------------------------------------------------------
    print("STEP 3: Continue with filling depressions and watershed analysis")
    #proc_params = {
    #    'input': ClippedRaster,
    #    'format': 0,
    #    '-f': False,
    #    'output': 'TEMPORARY_OUTPUT',
    #    'direction': 'TEMPORARY_OUTPUT',
    #    'areas': 'TEMPORARY_OUTPUT',
    #    'GRASS_REGION_PARAMETER': None,
    #    'GRASS_REGION_CELLSIZE_PARAMETER': 0,
    #    'GRASS_RASTER_FORMAT_OPT': '',
    #    'GRASS_RASTER_FORMAT_META': ''
    #}

    #results = processing.run("grass7:r.fill.dir", proc_params)

    proc_params ={'input':ClippedRaster,
        '-k':False,
        'mode':0,
        '-m':False,
        'distance':3,
        'minimum':None,
        'maximum':None,
        'power':2,
        'cells':8,
        'output':'TEMPORARY_OUTPUT',
        'uncertainty':'TEMPORARY_OUTPUT',
        'GRASS_REGION_PARAMETER':None,
        'GRASS_REGION_CELLSIZE_PARAMETER':0,
        'GRASS_RASTER_FORMAT_OPT':'',
        'GRASS_RASTER_FORMAT_META':''
    }

    results =  processing.run("grass7:r.fill.stats", proc_params)

    FILLED_DEM = results['output']
    FILLED_DEM = QgsRasterLayer(FILLED_DEM, "FILLED_DEM")
    QgsProject.instance().addMapLayer(FILLED_DEM)

    proc_params = {
        'elevation': FILLED_DEM,
        'depression': None,
        'flow': None,
        'disturbed_land': None,
        'blocking': None,
        'threshold': 100,
        'max_slope_length': None,
        'convergence': 5,
        'memory': 300,
        '-s': False,
        '-m': False,
        '-4': False,
        '-a': False,
        '-b': False,
        'accumulation': 'TEMPORARY_OUTPUT',
        'drainage': 'TEMPORARY_OUTPUT',
        'basin': 'TEMPORARY_OUTPUT',
        'stream': 'TEMPORARY_OUTPUT',
        'half_basin': 'TEMPORARY_OUTPUT',
        'length_slope': 'TEMPORARY_OUTPUT',
        'slope_steepness': 'TEMPORARY_OUTPUT',
        'tci': 'TEMPORARY_OUTPUT',
        'spi': 'TEMPORARY_OUTPUT',
        'GRASS_REGION_PARAMETER': None,
        'GRASS_REGION_CELLSIZE_PARAMETER': 0,
        'GRASS_RASTER_FORMAT_OPT': '',
        'GRASS_RASTER_FORMAT_META': ''
    }

    results = processing.run("grass7:r.watershed", proc_params)
    STREAM = results['stream']
    STREAM = QgsRasterLayer(STREAM, "STREAM")
    QgsProject.instance().addMapLayer(STREAM)

    DRAINAGE = results['drainage']
    DRAINAGE = QgsRasterLayer(DRAINAGE, "DRAINAGE")
    QgsProject.instance().addMapLayer(DRAINAGE)

    ACCUMULATION = results['accumulation']
    ACCUMULATION = QgsRasterLayer(ACCUMULATION, "ACCUMULATION")
    QgsProject.instance().addMapLayer(ACCUMULATION)

    # Create an absolute value version of the accumulation raster using Raster Calculator
    abs_acc_params = {
        'EXPRESSION': 'abs("ACCUMULATION@1")',
        'LAYERS': [ACCUMULATION],
        'CELLSIZE': 0,
        'EXTENT': None,
        'CRS': None,
        'OUTPUT': 'TEMPORARY_OUTPUT'
    }

    abs_result = processing.run("qgis:rastercalculator", abs_acc_params)
    ABS_ACCUMULATION = QgsRasterLayer(abs_result['OUTPUT'], "ABS_ACCUMULATION")
    QgsProject.instance().addMapLayer(ABS_ACCUMULATION)


    # ----------------------------------------------------------
    # STEP 5: Build and export the flow matrix and Sankey data
    # ----------------------------------------------------------
    output_path = current_folder_path + '/parcel_flow_matrix.csv'
    flow_matrix = create_flow_matrix_with_sink(parcels, ABS_ACCUMULATION, DRAINAGE)
    # convert to fraction of row total
    flow_matrix_frac = flow_matrix.div(flow_matrix['TOTAL_IN'], axis='rows')
    flow_matrix_frac.to_csv(output_path)
    # sankey_data = create_sankey_data(flow_matrix)

    print("Flow matrix created successfully!")
    print(f"saved output to '{output_path}'...")
    print(f"Matrix dimensions: {flow_matrix.shape}")
    print(f"Total flow in system: {flow_matrix.iloc[:-2, :-2].sum().sum()}")
    print(f"Total flow to sink: {flow_matrix.loc[:, 'SINK'].sum()}")
    return output_path
