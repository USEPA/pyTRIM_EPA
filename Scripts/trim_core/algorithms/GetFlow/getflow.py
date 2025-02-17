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

### START: Samuel's GetFlow_V7 utility functions
# (copied 100% as-is from GetFlow_V7, the Dec 31 2024 version)
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

def get_points_along_line(line_geom, interval):
    """Sample points along a line geometry at regular intervals"""
    points = []
    
    # Handle different geometry types
    if line_geom.isMultipart():
        # For multipart geometries, process each part
        for part in line_geom.asGeometryCollection():
            if part.type() == QgsWkbTypes.LineGeometry:
                length = part.length()
                current_distance = 0
                while current_distance <= length:
                    point = part.interpolate(current_distance)
                    points.append(point.asPoint())
                    current_distance += interval
    else:
        # For single part geometries
        length = line_geom.length()
        current_distance = 0
        while current_distance <= length:
            point = line_geom.interpolate(current_distance)
            points.append(point.asPoint())
            current_distance += interval
    
    return points

def analyze_flow_at_boundary(boundary, accum_layer, direction_layer):
    """Analyze flow across a specific boundary"""
    # Get sample points along the boundary
    sample_interval = direction_layer.rasterUnitsPerPixelX()
    points = get_points_along_line(boundary['boundary'], sample_interval)
    
    # Get flow values at each point
    total_flow = 0
    flow_direction = 0  # net flow direction (positive: 1->2, negative: 2->1)
    
    for point in points:
        accum_value = accum_layer.dataProvider().identify(
            point, QgsRaster.IdentifyFormatValue).results()[1]
        
        direction_value = direction_layer.dataProvider().identify(
            point, QgsRaster.IdentifyFormatValue).results()[1]
        
        if accum_value is not None and direction_value is not None:
            # Determine if flow is from parcel1 to parcel2 based on direction
            flow_vector = get_flow_vector(direction_value)
            boundary_vector = get_boundary_vector_for_point(point, boundary['boundary'])
            
            if vector_dot_product(flow_vector, boundary_vector) > 0:
                total_flow += accum_value
                flow_direction += 1
            else:
                total_flow -= accum_value
                flow_direction -= 1
    
    return total_flow, flow_direction

def get_flow_vector(direction):
    """Convert GRASS flow direction (1-8) to vector"""
    directions = {
        1: (1, 0),
        2: (1, 1),
        3: (0, 1),
        4: (-1, 1),
        5: (-1, 0),
        6: (-1, -1),
        7: (0, -1),
        8: (1, -1)
    }
    return directions.get(int(direction) if direction is not None else 0, (0, 0))

def get_boundary_vector_for_point(point, boundary_geom):
    """Get normalized boundary vector at a specific point"""
    # Find the closest segment to the point
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
                
                # Calculate distance from point to segment
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
    
    # Calculate the projection of the point onto the line
    line_length_squared = (x2 - x1)**2 + (y2 - y1)**2
    if line_length_squared == 0:
        return start
    
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / line_length_squared))
    
    return QgsPointXY(x1 + t * (x2 - x1), y1 + t * (y2 - y1))

def vector_dot_product(v1, v2):
    """Calculate dot product of two vectors"""
    return v1[0]*v2[0] + v1[1]*v2[1]

def create_flow_matrix(parcels_layer, accum_layer, direction_layer):
    """Create flow matrix between all parcels"""
    # Get all parcel titles
    titles = [f[TEMP_PARCEL_NAME_COL] for f in parcels_layer.getFeatures()]
    
    # Initialize flow matrix
    flow_matrix = pd.DataFrame(0, index=titles, columns=titles)
    
    # Get boundaries between parcels
    boundaries = get_parcel_boundaries(parcels_layer)
    
    # Analyze flow across each boundary
    for boundary in boundaries:
        total_flow, flow_direction = analyze_flow_at_boundary(
            boundary, accum_layer, direction_layer)
        
        if flow_direction > 0:
            flow_matrix.loc[boundary['parcel1'], boundary['parcel2']] = total_flow
        else:
            flow_matrix.loc[boundary['parcel2'], boundary['parcel1']] = abs(total_flow)
    
    return flow_matrix
### END: Samuel's GetFlow_V7 utility functions

def run_getflow_v7(parcels):
    # make it fast
    print(f"TIBSV7 RUN_GETFLOW_V7 FAKE ({type(parcels)}): {parcels}")
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

    print(f"TIBSV7 layered")

    # CLIP RASTER BY MASK LAYER
    proc_params = {
        'INPUT': dem_raster_layer,
        'MASK': parcel_layer,
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

    print(f"TIBSV7 run raster clipping...")

    # Run the raster clipping algorithm
    result = processing.run("gdal:cliprasterbymasklayer", proc_params)
    print(f"TIBSV7 result: {type(result)}")
    ClippedRaster = QgsRasterLayer(result['OUTPUT'], "ClippedRaster")
    print(f"TIBSV7 clipped raster: {type(ClippedRaster)}")
    QgsProject.instance().addMapLayer(ClippedRaster)
    print(f"TIBSV7 fill dem...")

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

    ### FILL DEM ###
    proc_params= {'DEM': ClippedRaster,
                  'FILLED':'TEMPORARY_OUTPUT',
                  'SINKS':'TEMPORARY_OUTPUT',
                  'DZFILL':0.01}

    # trying turning this off altogether...
    if False:
        print(f"TIBSV7 THIS NEXT LINE IS SLOW...")
        # changed from saga to sagang
        results = processing.run("sagang:fillsinksqmofesp",proc_params )
        print(f"TIBSV7 PAST!")
        FILLED_DEM = results['FILLED']
        FILLED_DEM = QgsRasterLayer(FILLED_DEM, "FILLED_DEM")
        QgsProject.instance().addMapLayer(FILLED_DEM)
    else:
        FILLED_DEM = ClippedRaster

    ### GET DIRECTION ###

    proc_params = {
        'elevation': FILLED_DEM,
        'depression':None,
        'flow':None,
        'disturbed_land':None,
        'blocking':None,
        'threshold':100,
        'max_slope_length':None,
        'convergence':5,
        'memory':300,
        '-s':False,
        '-m':False,
        '-4':False,
        '-a':False,
        '-b':False,
        'accumulation':'TEMPORARY_OUTPUT',
        'drainage':'TEMPORARY_OUTPUT',
        'basin':'TEMPORARY_OUTPUT',
        'stream':'TEMPORARY_OUTPUT',
        'half_basin':'TEMPORARY_OUTPUT',
        'length_slope':'TEMPORARY_OUTPUT',
        'slope_steepness':'TEMPORARY_OUTPUT',
        'tci':'TEMPORARY_OUTPUT',
        'spi':'TEMPORARY_OUTPUT',
        'GRASS_REGION_PARAMETER':None,
        'GRASS_REGION_CELLSIZE_PARAMETER':0,
        'GRASS_RASTER_FORMAT_OPT':'',
        'GRASS_RASTER_FORMAT_META':''}

    results = processing.run("grass7:r.watershed", proc_params)
    STREAM = results['stream']
    STREAM = QgsRasterLayer(STREAM, "STREAM")
    QgsProject.instance().addMapLayer(STREAM)

    results = processing.run("grass7:r.watershed", proc_params)
    DRAINAGE = results['drainage']
    DRAINAGE = QgsRasterLayer(DRAINAGE, "DRAINAGE")
    QgsProject.instance().addMapLayer(DRAINAGE)

    results = processing.run("grass7:r.watershed", proc_params)
    ACCUMULATION = results['accumulation']
    ACCUMULATION = QgsRasterLayer(ACCUMULATION, "ACCUMULATION")
    QgsProject.instance().addMapLayer(ACCUMULATION)

    # Create the flow matrix
    flow_matrix = create_flow_matrix(parcels, ACCUMULATION, DRAINAGE)

    # Save to CSV
    flow_matrix.to_csv(current_folder_path + '/parcel_flow_matrix.csv')













"""
def run_getflow(parcels):
    print(f"OLD VERSION - ABANDONING!")
    return

    # make it fast
    print(f"TIBS RUN_GETFLOW FAKE ({type(parcels)}): {parcels}")
    sep = os.path.sep

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
    # import code; code.interact(local=locals())

    # Paths to your data
    current_folder_path = os.path.realpath(os.path.dirname(__file__))
    print(f"TIBS let's look in '{current_folder_path}'...")
    dem_raster_layer = current_folder_path + f"{sep}USGS_1_n36w083_20220512.tif"
    # parcel_layer = current_folder_path + r"\Parcels\Durham_Parcels.geojson"
    # qgis_project_file = current_folder_path + r"\GetFlow_2.qgs"  # Specify the correct project file path
    parcel_layer = convert_to_geojson.GeoJson(parcels).convert_json()
    print(f"TIBS converted ({parcel_layer})")

    # Load parcels and DEM layers
    parcels = QgsVectorLayer(parcel_layer, "Parcels", "ogr")
    dem = QgsRasterLayer(dem_raster_layer, "DEM")

    # Add layers to the project
    QgsProject.instance().addMapLayer(parcels)
    QgsProject.instance().addMapLayer(dem)

    print(f"TIBS layered")

    # CLIP RASTER BY MASK LAYER
    proc_params = {
        'INPUT': dem_raster_layer,
        'MASK': parcel_layer,
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

    print(f"TIBS run raster clipping...")

    # Run the raster clipping algorithm
    result = processing.run("gdal:cliprasterbymasklayer", proc_params)
    print(f"TIBS result: {type(result)}")
    print(f"ACTUAL RESULT: {result}")

    # foo = result['OUTPUT']
    # bar = "/app/pytrim_getflow_src/USGS_1_n36w083_20220512.tif"
    # print(f"SANITY CHECK: '{foo}' exists? {os.path.exists(foo)}. '{bar}' exists? {os.path.exists(bar)}")
    # import shutil
    # shutil.copyfile(foo, "/app/pytrim_getflow_src/tibs.tif")
    # print(f"COPIED!")

    ClippedRaster = QgsRasterLayer(result['OUTPUT'], "ClippedRaster")
    print(f"TIBS clipped raster: {type(ClippedRaster)}")
    QgsProject.instance().addMapLayer(ClippedRaster)

    print(f"TIBS fill dem...")
    print(f"EARLY QUIT")
    return


    ### FILL DEM ###
    proc_params= {'DEM': ClippedRaster,
                  'FILLED':'TEMPORARY_OUTPUT',
                  'SINKS':'TEMPORARY_OUTPUT',
                  'DZFILL':0.01}

    results = processing.run("sagang:fillsinksqmofesp",proc_params )
    FILLED_DEM = results['FILLED']
    FILLED_DEM = QgsRasterLayer(FILLED_DEM, "FILLED_DEM")
    QgsProject.instance().addMapLayer(FILLED_DEM)

    ### GET DIRECTION ###
    print(f"TIBS get direction...")

    #NO LONGER NEEDED GET DRAINAGE FROM TOOL BELOW
    # proc_params = {'DEM': FILLED_DEM ,
                   # 'DIRECTION':'TEMPORARY_OUTPUT',
                   # 'CONNECTION':'TEMPORARY_OUTPUT',
                   # 'ORDER':'TEMPORARY_OUTPUT',
                   # 'BASIN':'TEMPORARY_OUTPUT',
                   # 'SEGMENTS':'TEMPORARY_OUTPUT',
                   # 'BASINS':'TEMPORARY_OUTPUT',
                   # 'NODES':'TEMPORARY_OUTPUT',
                   # 'THRESHOLD':5}

    # results = processing.run("saga:channelnetworkanddrainagebasins", proc_params)
    # DIRECTION = results['DIRECTION']
    # DIRECTION = QgsRasterLayer(DIRECTION, "DIRECTION")
    # QgsProject.instance().addMapLayer(DIRECTION)

    proc_params = {
        'elevation': FILLED_DEM,
        'depression':None,
        'flow':None,
        'disturbed_land':None,
        'blocking':None,
        'threshold':100,
        'max_slope_length':None,
        'convergence':5,
        'memory':300,
        '-s':False,
        '-m':False,
        '-4':False,
        '-a':False,
        '-b':False,
        'accumulation':'TEMPORARY_OUTPUT',
        'drainage':'TEMPORARY_OUTPUT',
        'basin':'TEMPORARY_OUTPUT',
        'stream':'TEMPORARY_OUTPUT',
        'half_basin':'TEMPORARY_OUTPUT',
        'length_slope':'TEMPORARY_OUTPUT',
        'slope_steepness':'TEMPORARY_OUTPUT',
        'tci':'TEMPORARY_OUTPUT',
        'spi':'TEMPORARY_OUTPUT',
        'GRASS_REGION_PARAMETER':None,
        'GRASS_REGION_CELLSIZE_PARAMETER':0,
        'GRASS_RASTER_FORMAT_OPT':'',
        'GRASS_RASTER_FORMAT_META':''}

    print(f"TIBS run watershed...")

    results = processing.run("grass7:r.watershed", proc_params)
    STREAM = results['stream']
    STREAM = QgsRasterLayer(STREAM, "STREAM")
    QgsProject.instance().addMapLayer(STREAM)

    print(f"TIBS run watershed again...")

    results = processing.run("grass7:r.watershed", proc_params)
    DRAINAGE = results['drainage']
    DRAINAGE = QgsRasterLayer(DRAINAGE, "DRAINAGE")
    QgsProject.instance().addMapLayer(DRAINAGE)

    print(f"TIBS run watershed a third time?...")
    results = processing.run("grass7:r.watershed", proc_params)
    ACCUMULATION = results['accumulation']
    ACCUMULATION = QgsRasterLayer(ACCUMULATION, "ACCUMULATION")
    QgsProject.instance().addMapLayer(ACCUMULATION)

    print(f"TIBS make numpy array...")

    # Convert raster data to a NumPy array
    provider = ACCUMULATION.dataProvider()
    extent = provider.extent()
    rows = ACCUMULATION.height()
    columns = ACCUMULATION.width()
    block = provider.block(1, extent, columns, rows)
    array = np.array(block.values)

    # Calculate the 20th percentile value
    percentile_value = np.percentile(array, 20)

    print(f"20th Percentile Value: {percentile_value}")



    # Function to calculate bearing in degrees
    def bearing(p1, p2):
        x_diff = p2.x() - p1.x()
        y_diff = p2.y() - p1.y()
        return math.degrees(math.atan2(y_diff, x_diff))

    # Function to move points by bearing and distance
    def move_point_by_bearing(point, distance, bearing_degrees):
        dx = distance * math.cos(math.radians(bearing_degrees))
        dy = distance * math.sin(math.radians(bearing_degrees))
        return QgsPointXY(point.x() + dx, point.y() + dy)

    # Initialize lists to store the points data
    points_data = []

    # Loop through the features in the parcel layer
    for feature in parcel_layer.getFeatures():
        # Get the centroid of the parcel
        parcel_centroid = feature.geometry().centroid().asPoint()

        # Clip the DEM raster to the extent of the parcel feature
        clip_extent = feature.geometry().boundingBox()
        clipped_raster_path = os.getcwd() + "/in_memory/Raster_Clipped.tif"
        processing.runAndLoadResults("gdal:cliprasterbyextent", {
            'INPUT': dem_raster_layer,
            'PROJWIN': f"{clip_extent.xMinimum()} {clip_extent.xMaximum()} {clip_extent.yMinimum()} {clip_extent.yMaximum()}",
            'NODATA': -3.402823e+038,
            'OPTIONS': '',
            'DATA_TYPE': 0,
            'EXTRA': '',
            'OUTPUT': clipped_raster_path
        })

        # Fill the clipped raster
        filled_raster_path = os.getcwd() + "/in_memory/Raster_Filled.tif"
        processing.runAndLoadResults("gdal:fillnodata", {
            'INPUT': clipped_raster_path,
            'BAND': 1,
            'DISTANCE': 0,
            'RESULTS': filled_raster_path
        })

        # ... Continue with the rest of the script ...

        # Move points by bearing and distance
        distance = 0.00005
        parcel_name = feature["ParcelName"]
        direction = feature["Direction"]
        accu = feature["Accu"]
        bearing_angle = feature["Direction_Angle"]

        new_point = move_point_by_bearing(parcel_centroid, distance, bearing_angle)

        # Store the point data
        points_data.append([
            QgsGeometry.fromPointXY(new_point),
            new_point.x(),
            new_point.y(),
            bearing_angle,
            parcel_name,
            direction,
            accu
        ])

    # Create a new memory layer to store the points data
    final_points_layer = QgsVectorLayer("Point?crs=EPSG:4326", "Pour_Points_Final", "memory")
    provider = final_points_layer.dataProvider()
    fields = QgsFields()
    fields.append(QgsField("SHAPE", QVariant.Point))
    fields.append(QgsField("POINT_X", QVariant.Double))
    fields.append(QgsField("POINT_Y", QVariant.Double))
    fields.append(QgsField("Direction_Angle", QVariant.Double))
    fields.append(QgsField("ParcelName", QVariant.String))
    fields.append(QgsField("Direction", QVariant.Long))
    fields.append(QgsField("Accu", QVariant.Double))
    provider.addAttributes(fields)

    final_points_layer.updateFields()
    provider.addFeatures([QgsFeature(fields, p) for p in points_data])

    # Save the layer to the project and add it to the map
    QgsProject.instance().addMapLayer(final_points_layer)

    # ADD TO-PARCEL OVERLAP
    joined_layer = processing.run("native:joinbylocation", {
        'INPUT': final_points_layer,
        'JOIN': parcel_layer,
        'PREDICATE': [0],  # Intersect
        'JOIN_FIELDS': ['ParcelName'],
        'METHOD': 0,  # One to one
        'DISCARD_NONMATCHING': False,
        'PREFIX': '',
        'OUTPUT': 'memory:'
    })['OUTPUT']

    # DIRECTION_ANGLE RADIANS TO DEGREES
    fields = joined_layer.fields()
    joined_layer.startEditing()
    joined_layer.addAttribute(QgsField("Direction_Degrees", QVariant.Int))
    for feature in joined_layer.getFeatures():
        direction_angle = feature["Direction_Angle"]
        feature["Direction_Degrees"] = math.degrees(direction_angle)
        joined_layer.updateFeature(feature)
    joined_layer.commitChanges()

    # Delete unnecessary fields
    fields_to_delete = ['Join_Count', 'TARGET_FID', 'ParcelName']
    joined_layer.startEditing()
    for field_name in fields_to_delete:
        joined_layer.deleteAttribute(fields.indexFromName(field_name))
    joined_layer.commitChanges()

    # Save the joined layer to the project and add it to the map
    QgsProject.instance().addMapLayer(joined_layer)



    path = os.getcwd()
    AttributeTable = pd.read_csv(path + "\\FlowPoints.csv", sep=",")



    Flow_PivotTable = pd.pivot_table(AttributeTable, values ="Accu", index=["Parcel_Name_TO"], columns=["Parcel_Name_FROM"], aggfunc=np.sum,margins=True)

    Flow_PivotTable_Avg = Flow_PivotTable.div(Flow_PivotTable.iloc[:,-1], axis=0)
    #Flow_PivotTable_Avg = Flow_PivotTable_Avg*100

    test = AttributeTable['Parcel_Name_FROM']
    Column_List = set(test)
    Column_List = sorted(Column_List)
    Column_List.insert(0,Column_List.pop(Column_List.index("Sink")))




    Flow_PivotTable_Avg =( Flow_PivotTable_Avg.drop(["Sink","All"],axis=0))

    Column_List = set(test)
    Column_List = sorted(Column_List)
    Column_List.insert(0,Column_List.pop(Column_List.index("Sink")))
    Column_List.append("All")
    print(Column_List)


    Flow_PivotTable_Avg = Flow_PivotTable_Avg.reindex(Column_List, axis=1)


    Flow_PivotTable_Avg.to_csv(path + "\\GetFlow_Matrix.csv")

    qgs.exitQgis()
"""
