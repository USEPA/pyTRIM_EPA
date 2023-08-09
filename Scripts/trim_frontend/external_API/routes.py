import os
import pandas as pd
import json
import numpy as np
import re
import shapefile
import traceback
import subprocess

from flask import Blueprint, request
from flask_security import login_required
from custom.flask_api import ApiException, ApiResult
from trim_frontend import api
from ..utils.logging import make_logger
from .helpers import UsdaApi, UsleClimateApi, convert_to_geojson
from pyproj import CRS, Transformer
from trim_db import ParcelService
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


external_api_soil = Blueprint('external_api_soil', __name__)
external_api_r = Blueprint('external_api_r', __name__)
api.use_api_errors(external_api_soil)
api.use_api_errors(external_api_r)


@external_api_soil.route('/api/soildata/<string:tillage>', methods=['GET'])
@login_required
def get_soil_data(tillage):
    logger = make_logger('external_api_call')
    logger.info(f"Obtaining parcel soil data from USDA.gov")
    try:
        from_url = request.referrer
        this_scenario_id = int(re.findall('/scenario/(\d+)/', from_url)[0])
        if not this_scenario_id:
            raise ApiException("No Scenario defined")
        p = ParcelService.get_all(scenario_id=this_scenario_id)
        parcels = {}
        if p is not None:
            for this_p in p:
                this_parcel_data = this_p.as_serializable()
                parcels[this_parcel_data['name']] = [(t[1], t[0]) for t in this_parcel_data['vertices']]
        sd = SoilData(vert_dict=parcels)
        # no_till_soil_data_json, tilled_soil_data_json = sd.run()
        sd.run()
        no_till_soil_data_json = sd.scenario_no_till_results
        tilled_soil_data_json = sd.scenario_tilled_results
    except Exception as e:
        logger.error(traceback.format_exc())

    if tillage == "till":
        result_soil_data_json = ApiResult(tilled_soil_data_json)
    elif tillage == "notill":
        result_soil_data_json = ApiResult(no_till_soil_data_json)
    elif tillage == "both":
        result_soil_data_json = {"tilled_data": tilled_soil_data_json,
                                 "no_till_data": no_till_soil_data_json}
    return result_soil_data_json


@external_api_r.route('/api/usledata/', methods=['GET'])
@login_required
def get_soil_data():
    logger = make_logger('external_api_call')
    logger.info(f"Obtaining parcel soil data from USDA.gov")
    try:
        from_url = request.referrer
        this_scenario_id = int(re.findall('/scenario/(\d+)/', from_url)[0])
        if not this_scenario_id:
            raise ApiException("No Scenario defined")
        p = ParcelService.get_all(scenario_id=this_scenario_id)
        parcels = {}
        for this_p in p:
            this_parcel_data = this_p.as_serializable()
            parcels[this_parcel_data['name']] = [(t[1], t[0]) for t in this_parcel_data['vertices']]
        usle_r_data = UsleRData()
        climate_data_file = ""
        result_usle_data_json = usle_r_data.run(parcels, climate_data_file)
        return result_usle_data_json
    except Exception as e:
        logger.error(traceback.format_exc())


class SoilData:
    parcel_vertices = {'E1': [(44.236310391612264, -85.510151405931794),
                              (44.209436004143171, -85.517352504159717),
                              (44.222723195504940, -85.579030393476131),
                              (44.254395937119604, -85.565839168593385),
                              (44.236310391612264, -85.510151405931794)]}

    no_tilled_layers = {'surface': {'bounds': [0, 1]},
                        'root': {'bounds': [1, 80]},
                        'vadose': {'bounds': [80, 220]},
                        'gw': {'bounds': [220, 250]}
                        }

    tilled_layers = {'surface': {'bounds': [0, 20]},
                     'root': {'bounds': [20, 80]},
                     'vadose': {'bounds': [80, 220]},
                     'gw': {'bounds': [220, 250]}
                     }

    scenario_tilled_results = {}

    scenario_no_till_results = {}

    def __init__(self, vert_file_name=None, vert_dict=None, no_till_layers=no_tilled_layers, tilled_layers=tilled_layers):
        if vert_file_name is not None:
            # with open(vert_file_name, 'r') as file:
            #     self.parcel_vertices = file.read()
            # shape = shapefile.Reader(vert_file_name)
            shape = self.read_shp(vert_file_name)
            self.parcel_vertices = shape
        elif vert_dict is not None:
            self.parcel_vertices = vert_dict
        self.parcel_vertices = self.get_parcel_vertices()

        self.no_tilled_layers = no_till_layers
        self.tilled_layers = tilled_layers

    @staticmethod
    def read_shp(shp_file):
        file_path = os.path.dirname(shp_file)
        file_name = os.path.basename(shp_file)
        # Find proj file using the filename of the shp file
        proj_file = file_path + os.sep + file_name.split(".")[0] + ".prj"
        proj = open(proj_file, "r").read()
        shapes = shapefile.Reader(shp_file)
        num_parcel = len(shapes)

        # Create a transformation object from x to WGS84
        from_crs = CRS(proj)
        to_crs = CRS.from_epsg(4326)
        transformer = Transformer.from_crs(from_crs, to_crs)

        # Create Dictionary of Polygons and Coordinates
        poly_dict = {}
        for i in range(0, num_parcel):
            s = shapes.shape(i)
            r = shapes.shapeRecord(i)
            poly_name = r.record[1]
            point_list = []
            for coord in s.points:
                transformed_point = transformer.transform(coord[0], coord[1])
                point_list.append(transformed_point)
            # poly_dict.append(point_list)
            poly_dict[poly_name] = point_list

        return poly_dict

    @staticmethod
    def calc_weighted_avg(df, val_col, wgt_col):
        return pd.DataFrame.sum(
            df[val_col] * (df[wgt_col]), min_count=1) / \
               (pd.NA if pd.DataFrame.sum(df[wgt_col][~pd.isna(df[val_col])]) == 0
                else pd.DataFrame.sum(df[wgt_col][~pd.isna(df[val_col])]))

    def compute_layer_averages(self, horizons, tilled=False):
        """computes layer thickness weighted average for each column of soil parameters"""
        layers = self.no_tilled_layers if not tilled else SoilData.tilled_layers
        horizons = horizons.sort_values(by=['hzdept_r', 'hzdepb_r', 'compname'])
        mu_averages_df = pd.DataFrame(columns=['mukey', 'area', 'layer', 'slope_r', 'kwfact', 'ph1to1h2o_r', 'om_r',
                                               'awc_r', 'sandtotal_r', 'slopelenusle_r'])
        this_mu = list(horizons.drop_duplicates(subset=['mukey'])['mukey'])
        this_tillage = "till" if tilled else "notill"
        current_row = 0
        for layer in layers:
            # Get all the horizons that overlap with this layer
            in_layer_horizons = horizons[layers[layer]['bounds'][0] <= horizons['hzdepb_r']]
            in_layer_horizons = in_layer_horizons[(in_layer_horizons['hzdept_r'] <= layers[layer]['bounds'][1])]
            if in_layer_horizons.__len__() == 0:
                # If no horizons in layer, then there is no data. In that case assign nans for each parameter
                initial_df = pd.DataFrame({'mukey': [horizons.head(n=1)['mukey'].values[0]],
                                           'area': [horizons.head(n=1)['area'].values[0]],
                                           'layer': [layer],
                                           'slope_r': [pd.NA],
                                           'kwfact': [pd.NA],
                                           'ph1to1h2o_r': [pd.NA],
                                           'om_r': [pd.NA],
                                           'awc_r': [pd.NA],
                                           'sandtotal_r': [pd.NA],
                                           'slopelenusle_r': [pd.NA]})
                mu_averages_df = pd.concat([mu_averages_df, initial_df], ignore_index=True)
                continue
            # Initialize dataframe object to hold averages for current layer
            layer_averages_df = pd.DataFrame(columns=list(horizons.columns))
            """There are 5 possible cases:     
            1. Layer overlaps a horizon partially at its (layer's) top
            2. Layer overlaps a horizon at its bottom
            3. Layer bounds and horizon bounds match exactly
            4. Horizon extends beyond both top and bottom bounds of layer
            5. Layer encapsulates horizon entirely."""
            # Get Horizons that are spilt at the top and the bottom of this layer (cases 1 and 2)
            split_horizon_top_df = in_layer_horizons[(layers[layer]['bounds'][0] < in_layer_horizons['hzdepb_r']) &
                                                     (in_layer_horizons['hzdepb_r'] <= layers[layer]['bounds'][1]) &
                                                     (in_layer_horizons['hzdept_r'] < layers[layer]['bounds'][0])]
            split_horizon_bottom_df = in_layer_horizons[(layers[layer]['bounds'][0] <= in_layer_horizons['hzdept_r']) &
                                                        (in_layer_horizons['hzdept_r'] < layers[layer]['bounds'][1]) &
                                                        (in_layer_horizons['hzdepb_r'] > layers[layer]['bounds'][1])]
            # Find the horizons that are fully contained within the layer bounds (cases 3, 4 and 5)
            no_split_horizons_df = in_layer_horizons[
                ~in_layer_horizons['@msdata:rowOrder'].isin(list(split_horizon_top_df['@msdata:rowOrder'])) &
                ~in_layer_horizons['@msdata:rowOrder'].isin(list(split_horizon_bottom_df['@msdata:rowOrder']))]

            # We need to make it a new df instance rather than copy of initial df to operate on it
            split_horizon_top_df = pd.DataFrame(split_horizon_top_df)
            split_horizon_bottom_df = pd.DataFrame(split_horizon_bottom_df)
            no_split_horizons_df = pd.DataFrame(no_split_horizons_df)
            # Calculate weighting coefficient based on thickness of horizon in the current layers top and bottom
            split_horizon_top_df['wgt_cf'] = (split_horizon_top_df['hzdepb_r'] - layers[layer]['bounds'][0]) / \
                                             (layers[layer]['bounds'][1] - layers[layer]['bounds'][0])
            split_horizon_bottom_df['wgt_cf'] = (layers[layer]['bounds'][1] - split_horizon_bottom_df['hzdept_r']) / \
                                                (layers[layer]['bounds'][1] - layers[layer]['bounds'][0])
            # Calculate weighting coefficient based on thickness of horizon of the layers that are not split
            no_split_horizons_df['wgt_cf'] = np.where(
                no_split_horizons_df['hzthk_r'] < (layers[layer]['bounds'][1] - layers[layer]['bounds'][0]),
                no_split_horizons_df['hzthk_r'] / (layers[layer]['bounds'][1] - layers[layer]['bounds'][0]),
                1)
            # Join dataframes
            weighted_horizons_df = pd.concat([split_horizon_top_df, no_split_horizons_df], ignore_index=True)
            weighted_horizons_df = pd.concat([weighted_horizons_df, split_horizon_bottom_df], ignore_index=True)

            # Find unique components by component name in the joint dataframe
            unique_comp = list(weighted_horizons_df.drop_duplicates(subset=['compname'])['compname'])

            # Loop over components to calculate the thickness weighted parameter averages foreach
            for comp in unique_comp:
                this_component_df = weighted_horizons_df[weighted_horizons_df['compname'] == comp]
                average_df = pd.DataFrame(this_component_df.head(n=1))
                average_df['slope_r'] = self.calc_weighted_avg(this_component_df, 'slope_r', 'wgt_cf')
                average_df['kwfact'] = this_component_df[this_component_df['hzdept_r'] == 0]['kwfact'] \
                    if layer == 'surface' else pd.NA
                average_df['ph1to1h2o_r'] = self.calc_weighted_avg(this_component_df, 'ph1to1h2o_r', 'wgt_cf')
                average_df['om_r'] = self.calc_weighted_avg(this_component_df, 'om_r', 'wgt_cf')
                average_df['awc_r'] = self.calc_weighted_avg(this_component_df, 'awc_r', 'wgt_cf')
                average_df['sandtotal_r'] = self.calc_weighted_avg(this_component_df, 'sandtotal_r', 'wgt_cf')
                average_df['slopelenusle_r'] = self.calc_weighted_avg(this_component_df, 'slopelenusle_r', 'wgt_cf')
                layer_averages_df = pd.concat([layer_averages_df, average_df], ignore_index=True)

            layer_averages_df["comppct_r"] = layer_averages_df["comppct_r"]/100
            this_layer_average = pd.DataFrame(columns=list(mu_averages_df.columns))
            this_layer_average['mukey'] = [layer_averages_df.head(n=1)['mukey'].values[0]]
            this_layer_average['area'] = [layer_averages_df.head(n=1)['area'].values[0]]
            this_layer_average['layer'] = layer
            this_layer_average['slope_r'] = [self.calc_weighted_avg(layer_averages_df, 'slope_r', 'comppct_r')]
            this_layer_average['kwfact'] = [self.calc_weighted_avg(layer_averages_df, 'kwfact', 'comppct_r')]
            this_layer_average['ph1to1h2o_r'] = [self.calc_weighted_avg(layer_averages_df, 'ph1to1h2o_r', 'comppct_r')]
            this_layer_average['om_r'] = [self.calc_weighted_avg(layer_averages_df, 'om_r', 'comppct_r')]
            this_layer_average['awc_r'] = [self.calc_weighted_avg(layer_averages_df, 'awc_r', 'comppct_r')]
            this_layer_average['sandtotal_r'] = [self.calc_weighted_avg(layer_averages_df, 'sandtotal_r', 'comppct_r')]
            this_layer_average['slopelenusle_r'] = [self.calc_weighted_avg(layer_averages_df, 'slopelenusle_r', 'comppct_r')]
            mu_averages_df = pd.concat([mu_averages_df, this_layer_average], ignore_index=True)

        return mu_averages_df

    def compute_parcel_averages(self, mu_df, total_area, tilled=False):
        df = pd.DataFrame(mu_df)

        df['wgt_mu_area'] = df['area'] / total_area

        # Initialize dataframe objects to hold final averages (tilled and no till)
        parcel_averages_df = pd.DataFrame(columns=list(df.columns))
        parcel_averages_df = parcel_averages_df.drop(['mukey', 'wgt_mu_area', 'area'], axis=1)

        t_layers = self.no_tilled_layers if not tilled else self.tilled_layers
        for t_layer in t_layers:
            this_layer_df = df[df['layer'] == t_layer]
            average_df = pd.DataFrame(this_layer_df.head(n=1))
            average_df = average_df.drop(['mukey', 'wgt_mu_area', 'area'], axis=1)
            # tilled_average_df['area'] = total_area
            average_df['layer'] = t_layer
            average_df['slope_r'] = self.calc_weighted_avg(this_layer_df, 'slope_r', 'wgt_mu_area')
            average_df['kwfact'] = self.calc_weighted_avg(this_layer_df, 'kwfact', 'wgt_mu_area') \
                if t_layer == 'surface' else pd.NA
            average_df['ph1to1h2o_r'] = self.calc_weighted_avg(this_layer_df, 'ph1to1h2o_r', 'wgt_mu_area')
            average_df['om_r'] = self.calc_weighted_avg(this_layer_df, 'om_r', 'wgt_mu_area')
            average_df['awc_r'] = self.calc_weighted_avg(this_layer_df, 'awc_r', 'wgt_mu_area')
            average_df['sandtotal_r'] = self.calc_weighted_avg(this_layer_df, 'sandtotal_r', 'wgt_mu_area')
            average_df['slopelenusle_r'] = self.calc_weighted_avg(this_layer_df, 'slopelenusle_r', 'wgt_mu_area')
            parcel_averages_df = pd.concat([parcel_averages_df, average_df], ignore_index=True)
        return parcel_averages_df

    def get_parcel_vertices(self):
        str_vert_list = {}
        for poly_list in self.parcel_vertices:
            # The required format is Latitude, Longitude
            # Flipping the order here
            elem = ",".join([str(this_tuple[1]) + " " + str(this_tuple[0])
                             for this_tuple in self.parcel_vertices[poly_list]])
            str_vert_list[poly_list] = elem
        return str_vert_list

    @staticmethod
    def get_soil_data(parcel_verts):
        parcel_dict = parcel_verts["pv"]
        r = UsdaApi.get_parcel_soil_data(parcel_coords=parcel_dict)
        return r

    def compute_parameters(self, parcel_data):
        r = parcel_data["pd"]
        this_parcel_vertices = parcel_data["pn"]
        tilled_results = {}
        no_till_results = {}
        r_dict = \
            r['soap:Envelope']['soap:Body']['RunQueryResponse']['RunQueryResult']['diffgr:diffgram']['NewDataSet'][
                'Table']
        df = pd.DataFrame(r_dict)
        df['area'] = pd.to_numeric(df.area)
        df['hzdept_r'] = pd.to_numeric(df.hzdept_r)
        df['hzdepb_r'] = pd.to_numeric(df.hzdepb_r)
        df['hzthk_r'] = pd.to_numeric(df.hzthk_r)
        df['comppct_r'] = pd.to_numeric(df.comppct_r)
        df['slope_r'] = pd.to_numeric(df.slope_r)
        df['kwfact'] = pd.to_numeric(df.kwfact)
        df['ph1to1h2o_r'] = pd.to_numeric(df.ph1to1h2o_r)
        df['om_r'] = pd.to_numeric(df.om_r)
        df['awc_r'] = pd.to_numeric(df.awc_r)
        df['sandtotal_r'] = pd.to_numeric(df.sandtotal_r)
        df['slopelenusle_r'] = pd.to_numeric(df.slopelenusle_r)

        unique_mu = df.drop_duplicates(subset=['mukey'])['mukey']
        t_df = pd.DataFrame()
        nt_df = pd.DataFrame()
        total_area = 0
        for mu in unique_mu:
            df_mu = df.query(f'mukey=="{mu}"')
            total_area = total_area + list(df_mu['area'])[0]
            this_mu_nt_df = pd.DataFrame(self.compute_layer_averages(df_mu))
            this_mu_t_df = pd.DataFrame(self.compute_layer_averages(df_mu, True))
            nt_df = pd.concat([nt_df, this_mu_nt_df])
            t_df = pd.concat([t_df, this_mu_t_df])

        # Calculate map unit averages for tilled case for given layer
        parcel_averages_df = self.compute_parcel_averages(t_df, total_area, tilled=True)
        # Calculate map unit averages for not tilled case for given layer
        no_till_parcel_averages_df = self.compute_parcel_averages(nt_df, total_area, tilled=False)

        tilled_results[this_parcel_vertices] = parcel_averages_df.to_json()
        no_till_results[this_parcel_vertices] = no_till_parcel_averages_df.to_json()
        return tilled_results, no_till_results

    def run(self):
        parcel_dicts = self.parcel_vertices
        tilled_results = {}
        no_till_results = {}
        parcel_vertices_names = list(parcel_dicts.keys())
        with ThreadPoolExecutor(max_workers=50) as t_executor:
            data_results = t_executor.map(self.get_soil_data, [{'pv': parcel_dicts[this_parcel_vertices],
                                                                'pn': parcel_vertices_names[i]}
                                                               for i, this_parcel_vertices in enumerate(parcel_dicts)])
        with ProcessPoolExecutor(max_workers=10) as p_executor:
            ave_results = p_executor.map(self.compute_parameters, [{'pd': data,
                                                                    'pn': parcel_vertices_names[i]}
                                                                   for i, data in enumerate(data_results)])
        for i, r in enumerate(ave_results):
            tilled_results[parcel_vertices_names[i]] = r[0][parcel_vertices_names[i]]
            no_till_results[parcel_vertices_names[i]] = r[1][parcel_vertices_names[i]]
        self.scenario_tilled_results = tilled_results
        self.scenario_no_till_results = no_till_results
        # return no_till_results, tilled_results


class UsleRData:
    @staticmethod
    def run(parcels, ClimateData):
        logger = make_logger('external_api_call')

        WORKING_DIR = os.path.dirname(__file__)
        qgis_interpreter = "C:\\Program Files\\QGIS 3.30.0\\apps\\Python39\\python3.exe"
        RUSLE_script = os.path.join(WORKING_DIR, "helpers", "RUSLE_Script_Final.py")

        parcels_fp = convert_to_geojson.GeoJson(parcels).convert_json()

        p = subprocess.Popen([qgis_interpreter, RUSLE_script, parcels_fp],                     
                            stdout = subprocess.PIPE, 
                            stderr = subprocess.PIPE)
        stdout, stderr = p.communicate()
        if stderr:
            logger.error(stderr.strip().decode('utf-8'))
        print("@@@@@@@@" + stdout.strip().decode('utf-8'))
        return stdout.strip().decode('utf-8')

