import collections
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

TEMP_PARCEL_NAME_COL = 'title' # actual TRIM parcels have a "title", not a "name"!

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

### START: Samuel's GetFlow_V10/13 utility functions
# (copied 99% as-is from GetFlow_V10, the April 2025 version), (and GetFlow_V13_LakesAndFlowLines.py, the Aug 2025 version)
#   replaced parcel_name_col --> TEMP_PARCEL_NAME_COL
# get_exterior_boundary and get_flow_vector actually come from V10; V13 script calls them but doesn't define them...similar issue existed when moving from v7->v10

# from GetFlowV10
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

# from GetFlowV10
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

# from GetFlowV13
def build_parcel_flow_matrix(parcels_layer, accum_raster, direction_raster, name_col='name'):
    """
    Compute how much flow (from accumulation raster) goes from each parcel to:
    - neighboring parcels, or
    - out of any parcel (to SINK)

    Returns:
    - raw flow matrix (absolute flow values)
    - percent flow matrix (row-normalized)
    """

    print(f"FIX ME {name_col=}")
    print(f"debug parcels layer START:")
    for f in parcels_layer.getFeatures():
        print(f"got {type(f)} / {f}")

        atts = f.attributeMap()
        print(f"debug parcels atts START:")
        for key in atts:
            val = atts.get(key, None)
            print(f"{key} ({type(key)}): {val} ({type(val)})")
        print(f"debug parcels atts END:")
    print(f"debug parcels layer END:")



    parcel_ids = [f[name_col] for f in parcels_layer.getFeatures()]
    flow_matrix = pd.DataFrame(0.0, index=parcel_ids, columns=parcel_ids + ['SINK'])

    # Get cell size for sampling
    cell_size = direction_raster.rasterUnitsPerPixelX()

    # Precompute boundaries
    boundary_points_per_parcel = collections.defaultdict(list)
    for feature in parcels_layer.getFeatures():
        geom = feature.geometry()
        pid = feature[name_col]
        boundary = get_exterior_boundary(geom)
        if boundary is None:
            continue
        length = boundary.length()
        dist = 0
        while dist <= length:
            point = boundary.interpolate(dist).asPoint()
            boundary_points_per_parcel[pid].append(point)
            dist += cell_size

    # Build parcel geometry lookup
    parcel_geoms = {f[name_col]: f.geometry() for f in parcels_layer.getFeatures()}

    matched = 0
    unmatched = 0

    # Analyze flow at each parcel boundary
    for pid, points in boundary_points_per_parcel.items():
        for pt in points:
            # Get accumulation and direction at this boundary point
            accum = accum_raster.dataProvider().identify(pt, QgsRaster.IdentifyFormatValue).results().get(1)
            direction = direction_raster.dataProvider().identify(pt, QgsRaster.IdentifyFormatValue).results().get(1)
            if accum is None or direction is None or accum <= 0:
                continue

            # Compute downstream flow point
            dx, dy = get_flow_vector(direction)
            next_pt = QgsPointXY(pt.x() + dx * cell_size, pt.y() + dy * cell_size)
            downstream_geom = QgsGeometry.fromPointXY(next_pt).buffer(cell_size * 5.00, 1)

            # Check if it flows into another parcel
            found_target = False
            for target_id, target_geom in parcel_geoms.items():
                if target_id == pid:
                    continue
                if target_geom.intersects(downstream_geom):
                    flow_matrix.loc[pid, target_id] += accum
                    found_target = True
                    matched += 1
                    break
            if not found_target:
                flow_matrix.loc[pid, 'SINK'] += accum
                unmatched += 1

    # Normalize to percentages of total outflow per parcel
    flow_matrix_pct = flow_matrix.div(flow_matrix.sum(axis=1), axis=0).fillna(0) * 100
    flow_matrix_pct = flow_matrix_pct.round(2)

    print(f"✅ Flow analysis complete. Matched: {matched}, To SINK: {unmatched}")
    return flow_matrix, flow_matrix_pct, matched, unmatched

### END: Samuel's GetFlow_V10/13 utility functions

def run_getflow_v13_for_scenario_id(scenario_id):
    print(f"v13 entrypoint for '{scenario_id}', alternate construction approach...")

    names_to_vertices = {}
    parcels = ParcelService.get_all(scenario_id=scenario_id)
    for p in parcels:
        # names_to_vertices[p.name] = p.vertices
        names_to_vertices[p.name] = [(v[1], v[0]) for v in p.as_serializable()['vertices']]
    # print(f"convert it ({names_to_vertices})")
    # parcels_for_this_scenario = json.dumps(names_to_vertices)
    parcels_for_this_scenario = names_to_vertices

    print(f"LOADED PARCELS: {parcels_for_this_scenario}")
    return run_getflow_v13(parcels_for_this_scenario)


# this is Samuel's GetFlow_V13_LakesAndFlowLines.py script with some changes -- separated out util functions, renamed a few things, etc.
def run_getflow_v13(parcels):
    # make it fast
    print(f"TIBSV13 RUN_GETFLOW_V13 ({type(parcels)}): {parcels}")
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
    print(f"TIBSV13 let's look in '{current_folder_path}'...")

    # qgis_project_file = current_folder_path + r"\GetFlow_2.qgs"  # Specify the correct project file path

    if USE_PRECANNED_TEST_DATA:
        # hardcoded temp test with good Samuel data
        parcel_layer = current_folder_path + "/Durham_Parcels.geojson"
        print(f"TIBSV13 using hardcoded parcels '{parcel_layer}'")

        dem_raster_layer = current_folder_path + f"{sep}USGS_1_n36w083_20220512.tif"
    else:
        # real conversion of passed-in parcels
        parcel_layer = convert_to_geojson.GeoJson(parcels).convert_json()
        print(f"TIBSV13 using real converted parcels '{parcel_layer}'")

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

    print(f"TIBSV13 PAST PARCEL/TIF SECTION ({USE_PRECANNED_TEST_DATA}): '{dem_raster_layer}' / '{parcel_layer}'")

    print(f"TIBSV13 converted ({parcel_layer})")

    # Load parcels and DEM layers
    parcels = QgsVectorLayer(parcel_layer, "Parcels", "ogr")
    dem = QgsRasterLayer(dem_raster_layer, "DEM")

    # Add layers to the project
    QgsProject.instance().addMapLayer(parcels)
    QgsProject.instance().addMapLayer(dem)

    print(f"TIBSV13 step 1...")
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


    print(f"TIBSV13 step 2...")
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
    """
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
    """
    # TEST END - dump out QgsRasterLayer


    print(f"TIBSV13 step 3...")
    # ----------------------------------------------------------
    # STEP 3: Continue with filling depressions and watershed analysis
    # ----------------------------------------------------------
    print("STEP 3: Continue with filling depressions and watershed analysis")

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

    print(f"TIBSV13 build_parcel_flow_matrix...")
    raw_matrix, percent_matrix, matched, unmatched = build_parcel_flow_matrix(parcels, ABS_ACCUMULATION, DRAINAGE, TEMP_PARCEL_NAME_COL)
    print(f"TIBSV13 build_parcel_flow_matrix...DONE")

    raw_output_path = f"{current_folder_path}{sep}parcel_raw_flow_matrix.csv"
    percent_output_path = f"{current_folder_path}{sep}parcel_percent_flow_matrix.csv"

    raw_matrix.to_csv(raw_output_path)
    percent_matrix.to_csv(percent_output_path)


    print("Parcel-to-parcel flow matrix created.")
    print(f"Raw flow matrix saved to '{raw_output_path}'")
    print(f"Percentage flow matrix saved to '{percent_output_path}'")
    print(f"Matched: {matched}, Unmatched (to SINK): {unmatched}")

    return (raw_output_path, percent_output_path)
