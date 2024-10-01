import math
import numpy as np
import pandas as pd
import os
from qgis.core import *
from Scripts.trim_frontend.external_API.helpers import convert_to_geojson

def run_getflow(parcels):
    # Paths to your data
    current_folder_path = os.path.realpath(os.path.dirname(__file__))
    dem_raster_layer = current_folder_path + r"\USGS_1_n36w083_20220512.tif"
    # parcel_layer = current_folder_path + r"\Parcels\Durham_Parcels.geojson"
    # qgis_project_file = current_folder_path + r"\GetFlow_2.qgs"  # Specify the correct project file path
    parcel_layer = convert_to_geojson(parcels)

    # Load parcels and DEM layers
    parcels = QgsVectorLayer(parcel_layer, "Parcels", "ogr")
    dem = QgsRasterLayer(dem_raster_layer, "DEM")

    # Add layers to the project
    QgsProject.instance().addMapLayer(parcels)
    QgsProject.instance().addMapLayer(dem)

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

    # Run the raster clipping algorithm
    result = processing.run("gdal:cliprasterbymasklayer", proc_params)
    ClippedRaster = QgsRasterLayer(result['OUTPUT'], "ClippedRaster")
    QgsProject.instance().addMapLayer(ClippedRaster)

    ### FILL DEM ###
    proc_params= {'DEM': ClippedRaster,
                  'FILLED':'TEMPORARY_OUTPUT',
                  'SINKS':'TEMPORARY_OUTPUT',
                  'DZFILL':0.01}

    results = processing.run("saga:fillsinksqmofesp",proc_params )
    FILLED_DEM = results['FILLED']
    FILLED_DEM = QgsRasterLayer(FILLED_DEM, "FILLED_DEM")
    QgsProject.instance().addMapLayer(FILLED_DEM)

    ### GET DIRECTION ###

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