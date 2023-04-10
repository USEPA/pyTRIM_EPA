import pandas as pd
import requests
#import numpy as np
import os, sys, json
import cs_USLE_climateAPI
from qgis.core import *

QGIS_ROOT = " ".join(sys.argv[1:])
WORKING_DIR = os.path.dirname(__file__)

# Initialize QGIS Application
QgsApplication.setPrefixPath(f"{QGIS_ROOT}/apps/qgis", True)
qgs = QgsApplication([], False)
qgs.initQgis()


import processing
from processing.core.Processing import Processing

Processing.initialize()


ClimateData = os.path.join(WORKING_DIR, "Inputs", "ClimateShapeFile.shp")
Parcels = os.path.join(WORKING_DIR, "Inputs", "Foundries_Parcels.shp")


def RUSLE(Parcels, ClimateData):
    # Import climate data shapefile layer
    Climate_layer = QgsVectorLayer(ClimateData, "ClimateData", "ogr")
    if not Climate_layer.isValid():
        print("Climate layer failed to load!")
    else:
        pass
        # QgsProject.instance().addMapLayer(Climate_layer)

    # Import parcels shapefile layer
    Parcels_layer = QgsVectorLayer(Parcels, "Parcels", "ogr")
    if not Parcels_layer.isValid():
        print("Parcels layer failed to load!")
    else:
        pass
        # QgsProject.instance().addMapLayer(Parcels_layer)

    # 1) Fix geometries on parcel layer
    parameter = {"INPUT": Parcels_layer, "OUTPUT": "memory: FixedParcels_1"}
    result = processing.run("native:fixgeometries", parameter)
    # FixedParcels_1 = QgsProject.instance().addMapLayer(result['OUTPUT'])
    FixedParcels_1 = result["OUTPUT"]

    # 2) Reproject fixed parcel layer
    parameter = {
        "INPUT": FixedParcels_1,
        "TARGET_CRS": QgsCoordinateReferenceSystem("ESRI:102003"),
        "OPERATION": "+proj=pipeline +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=aea +lat_0=37.5 +lon_0=-96 +lat_1=29.5 +lat_2=45.5 +x_0=0 +y_0=0 +ellps=GRS80",
        "OUTPUT": "memory:ReprojectedFixedParcels_2",
    }
    result = processing.run("native:reprojectlayer", parameter)
    # ReprojectedFixedParcels_2 = QgsProject.instance().addMapLayer(result['OUTPUT'])
    ReprojectedFixedParcels_2 = result["OUTPUT"]

    # 3) Add geometry to reprojected fixed parcels
    parameter = {
        "INPUT": ReprojectedFixedParcels_2,
        "CALC_METHOD": 0,
        "OUTPUT": "memory:AreaCalcReprojectedFixedParcels_3",
    }
    result = processing.run("qgis:exportaddgeometrycolumns", parameter)
    # AreaCalcReprojectedFixedParcels_3 = QgsProject.instance().addMapLayer(result['OUTPUT'])
    AreaCalcReprojectedFixedParcels_3 = result["OUTPUT"]

    # 4) Intersection
    parameter = {
        "INPUT": AreaCalcReprojectedFixedParcels_3,
        "OVERLAY": Climate_layer,
        "INPUT_FIELDS": [],
        "OVERLAY_FIELDS": [],
        "OVERLAY_FIELDS_PREFIX": "",
        "OUTPUT": "memory:Intersection_4",
    }
    # have to use ClimateData variable for overlay as opposed to Climate_layer variable
    result = processing.run("native:intersection", parameter)
    # Intersection_4 = QgsProject.instance().addMapLayer(result['OUTPUT'])
    Intersection_4 = result["OUTPUT"]

    # 5) Area Calculation
    parameter = {
        "INPUT": Intersection_4,
        "CALC_METHOD": 0,
        "OUTPUT": "memory:AreaCalcIntersection_5",
    }
    result = processing.run("qgis:exportaddgeometrycolumns", parameter)
    # AreaCalcIntersection_5 = QgsProject.instance().addMapLayer(result['OUTPUT'])
    AreaCalcIntersection_5 = result["OUTPUT"]

    # 6) Field calculator for percent area
    parameter = {
        "INPUT": AreaCalcIntersection_5,
        "FIELD_NAME": "Perc_Area",
        "FIELD_TYPE": 0,
        "FIELD_LENGTH": 10,
        "FIELD_PRECISION": 3,
        "FORMULA": ' "area_2" /  "area" ',
        "OUTPUT": "memory:PercentAreaCalc_6",
    }
    result = processing.run("native:fieldcalculator", parameter)
    # PercentAreaCalc_6 = QgsProject.instance().addMapLayer(result['OUTPUT'])
    PercentAreaCalc_6 = result["OUTPUT"]

    # 7) Convert Polygon Layer to Random Points Inside Polygon
    parameter = {
        "INPUT": PercentAreaCalc_6,
        "POINTS_NUMBER": 1,
        "MIN_DISTANCE": 0,
        "MIN_DISTANCE_GLOBAL": 0,
        "MAX_TRIES_PER_POINT": 10,
        "SEED": None,
        "INCLUDE_POLYGON_ATTRIBUTES": True,
        "OUTPUT": "memory:PercentAreaAsPoints_7",
    }
    result = processing.run("native:randompointsinpolygons", parameter)
    # PercentAreaAsPoints_7 = QgsProject.instance().addMapLayer(result['OUTPUT'])
    PercentAreaAsPoints_7 = result["OUTPUT"]

    # 8) Add XY Columns to Layer
    parameter = {
        "INPUT": PercentAreaAsPoints_7,
        "CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
        "PREFIX": "",
        "OUTPUT": "memory:AddXY_8",
    }
    result = processing.run("native:addxyfields", parameter)
    # AddXY_8 = QgsProject.instance().addMapLayer(result['OUTPUT'])
    AddXY_8 = result["OUTPUT"]

    # 9) Convert Attribute Table to Pandas DataFrame
    cols = [f.name() for f in AddXY_8.fields()]
    datagen = ([f[col] for col in cols] for f in AddXY_8.getFeatures())

    df = pd.DataFrame.from_records(data=datagen, columns=cols)

    df["R_Value"] = df.apply(lambda x: cs_USLE_climateAPI.UsleClimateApi.get_r_value(x["y"], x["x"]), axis=1)
    df["R_Value"] = df["R_Value"].astype(float).fillna(0.0)
    df["Area_Weighted_R"] = df["R_Value"] * df["Perc_Area"]

    results = df.groupby("PartName")["Area_Weighted_R"].agg(sum)

    return results


df = RUSLE(Parcels, ClimateData)
df.to_json(os.path.join(WORKING_DIR, "RUSLE_output.json"))
