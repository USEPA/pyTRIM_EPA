import json
import pandas as pd
import sqlalchemy as sa
from shapely.geometry import Polygon
from pyproj import CRS, Transformer
from pyproj import Geod
from shapely import wkt
from ..parameters.utils import ureg
from ..parameters.models import ParameterDefinition, CustomParameter
from ..utils.base import Model


__all__ = [
    'Parcel', 'VolumeElement', 'Media', 'Compartment',
    'CompartmentLink'
]

GLOBAL_WILDCARD = "$"


class Parcel(Model):
    name = sa.Column(sa.String(120), nullable=False)
    description = sa.Column(sa.String(250), nullable=True)

    scenario_id = sa.Column(
        sa.Integer(), sa.ForeignKey('scenario.id'), nullable=False
    )
    scenario = sa.orm.relationship(
        'Scenario', backref=sa.orm.backref('parcels', lazy='dynamic')
    )

    # Store as a string, but make a property to access as an array
    _vertices = sa.Column('vertices', sa.JSON(), nullable=False)

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
                self._vertices = value
            except json.JSONDecodeError:
                raise
        else:
            self._vertices = value

    @property
    def polygon(self):
        return Polygon(self.vertices)

    @property
    def utm_vertices(self):
        proj = 'PROJCS["WGS_1984_UTM_Zone_16N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-87.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'
        from_crs = CRS.from_epsg(4326)
        to_crs = CRS.from_wkt(proj)
        transformer = Transformer.from_crs(from_crs, to_crs)
        utm_vert = [transformer.transform(pt[1], pt[0]) for pt in self.vertices]
        return utm_vert

    @property
    def utm_polygon(self):
        return Polygon(self.utm_vertices)

    @property
    def area(self):
        # CAREFUL: we assume dimensions are in meters ...
        # return self.polygon.area * ureg('m^2')
        # CAREFUL-2: we assume ellipsoid is WGS84 ...
        # geod = Geod(ellps="WGS84")
        # poly = wkt.loads(
        #     f'''POLYGON (({", ".join([str(tpl[0]) + " " + str(tpl[1]) for tpl in self.vertices])}))''')
        # return abs(geod.geometry_area_perimeter(poly)[0]) * ureg('m^2')
        return self.utm_polygon.area * ureg('m^2')

    def get_volume_element(self, name):
        for ve in self.volume_elements:
            if ve.name == name or ve.standard_name == name:
                return ve
        return None

    @property
    def compartments(self):
        comps = []
        for ve in self.volume_elements:
            for c in ve.compartments:
                comps.append(c)
        return list(sorted(comps, key=lambda x: x.name))

    def get_compartment(self, name=None, media=None):
        if name is None and media is None:
            raise ValueError('Must supply either "name" or "media" argument')
        if media is not None:
            check = [c for c in self.compartments if c.media.isa(media)]
            if name is None:
                return check
        else:
            check = self.compartments
        for x in check:
            if x.name == name or x.standard_name == name:
                return x
        return None

    @property
    def has_air(self):
        for ve in self.volume_elements:
            if ve.name == "Air":
                return "Yes"
        return "No"

    @property
    def has_water(self):
        for ve in self.volume_elements:
            if ve.name == "SW":
                return "Yes"
        return "No"

    @property
    def has_land(self):
        for ve in self.volume_elements:
            if ve.name == "SurfSoil":
                return "Yes"
        return "No"

    @property
    def parcel_type(self):
        if self.has_air == "Yes":
            if self.has_water == "Yes":
                return "Water & Air"
            if self.has_land == "Yes":
                return "Land & Air"
            return "Air Only"
        if self.has_water == "Yes":
            return "Water Only"
        return "Land Only"

    @property
    def land_use(self):
        # No land use for air-only and land-only parcels
        if self.parcel_type in ["Air Only", "Water Only", "Water & Air"]:
            return "N/A"
        for c in self.compartments:
            # if c.media.isa('Surface_Water'):
            #     return 'Water'
            if c.media.isa('Coniferous_Forest'):
                return 'Coniferous Forest'
            if c.media.isa('Deciduous_Forest'):
                return 'Deciduous Forest'
            if c.media.isa('Agriculture'):
                return 'Agriculture - General'
            if c.media.isa('Grass'):
                return 'Grasses/Herbs'
            if c.media.isa('Tilled_Soil'):
                return 'Tilled Soil'
            if c.media.isa('Untilled_Soil'):
                return 'Untilled Soil'
        return 'Impervious'

    @property
    def has_farm_food_chain(self):
        if self.get_compartment("Farm"):
            return "Yes"
        return "No"

    @property
    def has_fish_food_web(self):
        aquatic_biota = [c for c in self.compartments if c.media.isa("Aquatic")]
        if len(aquatic_biota) > 0:
            return "Yes"
        return "No"

    @property
    def has_wetland(self):
        if self.get_compartment("Wetland"):
            return "Yes"
        return "No"

    @property
    def dust_load(self):
        air_comp = [c for c in self.compartments if c.media.isa("Air")]
        if len(air_comp) > 0:
            air_comp = air_comp[0]
            if air_comp.DustLoad:
                return air_comp.DustLoad.magnitude
            else:
                dust_load = air_comp.parameters.get("DustLoad").default_value if air_comp.parameters.get(
                    "DustLoad") else None
                return dust_load
        return None
        # for c in self.compartments:
        #     if c.name == "Air":
        #         dust_concentration = c.parameters["DustLoad"].value
        #         return dust_concentration
        # return None

    @property
    def dust_density(self):
        air_comp = [c for c in self.compartments if c.media.isa("Air")]
        if len(air_comp) > 0:
            air_comp = air_comp[0]
            if air_comp.DustDensity:
                return air_comp.DustDensity.magnitude
            else:
                dust_density = air_comp.parameters.get("DustDensity").default_value if air_comp.parameters.get(
                    "DustDensity") else None
                return dust_density
        return None
        # for c in self.compartments:
        #     if c.name == "Air":
        #         dust_density = c.parameters["DustDensity"].value
        #         return dust_density
        # return None

    @property
    def fraction_organic_matter_on_particulates(self):
        air_comp = [c for c in self.compartments if c.media.isa("Air")]
        if len(air_comp) > 0:
            air_comp = air_comp[0]
            if air_comp.FractionOrganicMatteronParticulates:
                try:
                    return air_comp.FractionOrganicMatteronParticulates.magnitude
                except AttributeError:  # TODO: Investigate why magnitude works for some and not for others???
                    return air_comp.FractionOrganicMatteronParticulates
            else:
                fraction_organic_matter_on_particulates = air_comp.parameters.get("FractionOrganicMatteronParticulates").default_value if air_comp.parameters.get(
                    "FractionOrganicMatteronParticulates") else None
                return fraction_organic_matter_on_particulates
        return None
        # for c in self.compartments:
        #     if c.name == "Air":
        #         fraction_organic_matter_on_particulates = c.parameters["FractionOrganicMatteronParticulates"].value
        #         return fraction_organic_matter_on_particulates
        # return None

    @property
    def air_density(self):  # TODO: This needs to be fixed so that parameters belonging to compartment domain should automatically associated with that compartment???
        air_comp = [c for c in self.compartments if c.media.isa("Air")]
        if len(air_comp) > 0:
            air_comp = air_comp[0]
            if air_comp.AirDensity:
                return air_comp.AirDensity.magnitude
            else:
                air_density = air_comp.parameters.get("AirDensity").default_value if air_comp.parameters.get("AirDensity") else None
                return air_density
        return None
        # for c in self.compartments:
        #     if c.media.isa("Air"):
        #         air_density = c.parameters["AirDensity"].value
        #         return air_density
        # return None

    @property
    def air_height(self):
        for ve in self.volume_elements.all():
            if "Air" in [a.name for a in list(ve.compartments)]:
                air_ind = [a.name for a in list(ve.compartments)].index("Air")
                return ve.compartments[air_ind].volume_element.height.m_as("m")
        return None

    @property
    def soil_tillage(self):
        is_tilled = "No"
        for c in self.compartments:
            if c.name == "Soil_Surface":
                st = c.parameters.get("soilTillage")
                if isinstance(st, ParameterDefinition):
                    val = int(st.default_value)
                elif isinstance(st, CustomParameter):
                    val = int(st.value)
                else:
                    raise AssertionError
                is_tilled = "Yes" if val == 1 else "No"
        return is_tilled

    @property
    def aquatic_diet_fractions(self):
        frc_diet = {
            'FractionDietAlgae': 0,
            'FractionDietMacrophyte': 0,
            'FractionDietZooplankton': 0,
            'FractionDietBenthicInvertebrate': 0,
            'FractionDietFishHerbivore': 0,
            'FractionDietFishBenthicOmnivore': 0,
            'FractionDietFishOmnivore': 0,
            'FractionDietFishBenthicCarnivore': 0,
            'FractionDietFishCarnivore': 0
        }
        diet_mat = {}
        for ve in self.volume_elements.all():
            if ve.name == 'SW' or ve.name == "Sed":
                for comp in ve.compartments.all():
                    if comp.media.isa("Benthic") or comp.media.isa("Water_Column") or comp.media.isa(
                            "Plankton") or comp.media.isa("Macrophyte"):
                        fd = frc_diet.copy()
                        for f, v in fd.items():
                            if comp.parameters.get(f):
                                fd[f] = comp.parameters.get(f).value

                        diet_mat[comp.name] = fd
        return diet_mat

    def aquatic_property(self, prop):
        apr = {}

        comps = [c for c in self.compartments if c.media.isa("Aquatic")]
        for c in comps:
            comp_name = c.name
            if c.parameters.get(prop) is not None:
                if c.parameters.get(prop).__tablename__ == "parameter_definition":
                    apr[f'{comp_name}'] = float("%0.4f" % c.parameters.get(prop).default_value)
                else:
                    apr[f'{comp_name}'] = float("%0.4f" % c.parameters.get(prop).value)
            else:
                apr[f'{comp_name}'] = None

        return apr

    @property
    def surface_soil_height(self):
        for ve in self.volume_elements.all():
            if 'Soil_Surface' in [a.name for a in list(ve.compartments)]:
                comp_ind = [a.name for a in list(ve.compartments)].index("Soil_Surface")
                return ve.compartments[comp_ind].volume_element.height.m_as("m")
        return None

    @property
    def root_soil_height(self):
        for ve in self.volume_elements.all():
            if 'Soil_Root_Zone' in [a.name for a in list(ve.compartments)]:
                comp_ind = [a.name for a in list(ve.compartments)].index("Soil_Root_Zone")
                return ve.compartments[comp_ind].volume_element.height.m_as("m")
        return None

    @property
    def vadose_soil_height(self):
        for ve in self.volume_elements.all():
            if 'Soil_Vadose_Zone' in [a.name for a in list(ve.compartments)]:
                comp_ind = [a.name for a in list(ve.compartments)].index("Soil_Vadose_Zone")
                return ve.compartments[comp_ind].volume_element.height.m_as("m")
        return None

    @property
    def groundwater_height(self):
        for ve in self.volume_elements.all():
            if 'Groundwater' in [a.name for a in list(ve.compartments)]:
                comp_ind = [a.name for a in list(ve.compartments)].index("Groundwater")
                return ve.compartments[comp_ind].volume_element.height.m_as("m")
        return None

    @property
    def total_erosion_rate(self):
        for c in self.compartments:
            if c.media.isa('Surface_Soil'):
                if c.parameters.get('TotalErosionRate'):
                    return c.parameters.get('TotalErosionRate').value
        return None

    # Each parcel should have a unique name in its scenario
    __table_args__ = (
        sa.UniqueConstraint('scenario_id', 'name'),
    )

    def wc_properties(self, p_name):
        c = [c for c in self.compartments if c.media.isa("Surface_Water")]
        if len(c) > 0:
            c = c[0]
        if p_name == "MeanWaterDepth":
            return c.volume_element.top - c.volume_element.bottom
        if c.parameters.get(p_name) is not None:
            if c.parameters.get(p_name).__tablename__ == "parameter_definition":
                return c.parameters.get(p_name).default_value
            else:
                return c.parameters.get(p_name).value
        return None

    def sed_properties(self, p_name):
        c = [c for c in self.compartments if c.media.isa("Sediment")]
        if len(c) > 0:
            c = c[0]
        if p_name == "MeanThickness":
            return c.volume_element.top - c.volume_element.bottom
        if c.parameters.get(p_name) is not None:
            if c.parameters.get(p_name).__tablename__ == "parameter_definition":
                return c.parameters.get(p_name).default_value
            else:
                return c.parameters.get(p_name).value
        return None

    @property
    def precipitation_rate(self):
        return 1

    @property
    def runoff_watershed_area(self):
        return 1e3

    @property
    def precip_seepage_frac_to_gw(self):
        return 0.001

    # TODO: Water body properties loads so slow! Why? Need a permanent fix!
    @property
    def seepage_vol_rate_to_gw(self):
        # if all([i is not None for i in [self.precipitation_rate, self.precip_seepage_frac_to_gw,
        #                                 self.runoff_watershed_area]]):
        #     return self.precipitation_rate * self.precip_seepage_frac_to_gw * self.runoff_watershed_area
        # return None
        return 1

    @property
    def precip_runoff_frac_to_sw(self):
        return 0.001

    @property
    def runoff_vol_rate_to_sw(self):
        # if all([i is not None for i in [self.precipitation_rate, self.precip_runoff_frac_to_sw,
        #                                 self.runoff_watershed_area]]):
        #     return self.precipitation_rate * self.precip_runoff_frac_to_sw * self.runoff_watershed_area
        # return None
        return 1

    @property
    def precipitation_vol_rate_to_sw(self):
        # if all([i is not None for i in [self.precipitation_rate, self.area]]):
        #     return self.precipitation_rate * self.area
        # return None
        return 4.8E6

    @property
    def wc_external_inflow(self):
        return 0

    @property
    def wc_discharge_vol_rate(self):
        # if all([i is not None for i in [self.runoff_vol_rate_to_sw, self.seepage_vol_rate_to_gw,
        #                                 self.wc_external_inflow, self.evaporation_vol_rate,
        #                                 self.precipitation_vol_rate_to_sw]]):
        #     return float('{:.5f}'.format(self.runoff_vol_rate_to_sw + self.seepage_vol_rate_to_gw + self.wc_external_inflow +
        #                                  self.precipitation_vol_rate_to_sw + self.precipitation_vol_rate_to_sw -
        #                                  self.evaporation_vol_rate))
        # return None
        return 6.2E6
        
    @property
    def wc_sed_discharge_rate(self):
        # if all([i is not None for i in [self.wc_properties("SuspendedSedimentConcentration"),
        #                                 self.wc_discharge_vol_rate]]):
        #     return self.wc_properties("SuspendedSedimentConcentration") * self.wc_discharge_vol_rate
        # return None
        return 3.13E5

    @property
    def evaporation_vol_rate(self):
        # if all([i is not None for i in [self.wc_properties("waterEvaporationRate"), self.area]]):
        #     return self.wc_properties("waterEvaporationRate") * self.area
        # return None
        return 3.3E6

    @property
    def sed_burial_vol_rate(self):
        # if all([i is not None for i in [self.wc_properties("ExternalSedimentInflow"), self.sed_soil_erosion_to_sw,
        #                                 self.wc_sed_discharge_rate, self.sed_properties("BedDensity"), self.area]]):
        #     return (self.wc_properties("ExternalSedimentInflow") + self.sed_soil_erosion_to_sw -
        #                                   self.wc_sed_discharge_rate) / (self.sed_properties("BedDensity") * self.area)
        # return None
        return 2.4992e-5

    @property
    def sed_deposition_vol_rate(self):
        # if all([i is not None for i in [self.wc_properties("SedimentDepositionVelocity"),
        #                                 self.wc_properties("SuspendedSedimentConcentration"),
        #                                 self.sed_properties("BedDensity")]]):
        #     return (self.wc_properties("SedimentDepositionVelocity") *
        #             self.wc_properties("SuspendedSedimentConcentration")) / self.sed_properties("BedDensity")
        # return None
        return 3.8462e-5

    @property
    def sed_resuspension_vel(self):
        # if all([i is not None for i in [self.sed_deposition_vol_rate, self.sed_burial_vol_rate,
        #                                 self.sed_properties("Porosity")]]):
        #     return (self.sed_deposition_vol_rate - self.sed_burial_vol_rate) / (1 - self.sed_properties("Porosity"))
        # return None
        return 6.2480e-5

    @property
    def sed_soil_erosion_to_sw(self):
        return 100

    def as_serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'vertices': self.vertices,
            'area': self.area,
            'hasAir': self.has_air,
            'airDensity': self.air_density,
            'airHeight': self.air_height,
            'surfaceSoilThickness': self.surface_soil_height,
            'rootSoilThickness': self.root_soil_height,
            'vadoseSoilThickness': self.vadose_soil_height,
            "groundwaterZoneThickness": self.groundwater_height,
            'parcelType': self.parcel_type,
            'hasLand': self.has_land,
            'landUse': self.land_use,
            'hasFarmFoodChain': self.has_farm_food_chain,
            'hasFishFoodWeb': self.has_fish_food_web,
            'hasWetland': self.has_wetland,
            'dustLoad': self.dust_load,
            'dustDensity': self.dust_density,
            'fractionOrganicMatteronParticulates': self.fraction_organic_matter_on_particulates,
            'soilTillage': self.soil_tillage,
            'totalErosionRate': self.total_erosion_rate,
            'aquatic_diet_fractions': self.aquatic_diet_fractions,
            'aquatic_biomass': self.aquatic_property("BiomassPerArea"),
            'aquatic_bw': self.aquatic_property("BW"),
            'precip_rate': self.precipitation_rate,
            'precip_runoff_watershed_area': self.runoff_watershed_area,
            'precip_seepage_vol_rate_to_GW': self.seepage_vol_rate_to_gw,
            'precip_runoff_vol_rate_to_SW': self.runoff_vol_rate_to_sw,
            'precip_vol_rate_to_SW': self.precipitation_vol_rate_to_sw,
            'sed_soil_erosion_to_SW': self.sed_soil_erosion_to_sw,
            'surface_water': None if self.parcel_type not in ["Water Only", "Water & Air"] else {
                'wc_props':  {
                    'flush_rate': 0.48,  # self.wc_properties("Flushes"),
                    'suspended_sed_conc': 0.05,  # self.wc_properties("SuspendedSedimentConcentration"),
                    'algae_density': 1.23E-2,  # self.wc_properties("AlgaeDensityInWaterColumn"),
                    'chloride_conc': 7,  # self.wc_properties("ChlorideConcentration"),
                    'chlorophyll_conc': 0.003,  # self.wc_properties("ChlorophyllConcentration"),
                    'mean_depth': 3.6,  # self.wc_properties("MeanWaterDepth"),
                    'evaporation_rate': 0.7,  # self.wc_properties("waterEvaporationRate"),
                    'evaporation_vol_rate': self.evaporation_vol_rate,
                    'suspended_organic_carbon': 0.05,  # self.wc_properties("OrganicCarbonContent"),
                    'water_ph': 8.5,  # self.wc_properties("pH"),
                    'sed_deposition_vel': 2,  # self.wc_properties("SedimentDepositionVelocity"),
                    'water_temp': 286.15,  # self.wc_properties("WaterTemperature"),
                    'sed_inflow': 0,  # self.wc_properties("ExternalSedimentInflow"),
                    'discharge_vol_rate': self.wc_discharge_vol_rate,
                    'sed_discharge_rate': self.wc_sed_discharge_rate
                },
                'sed_props': {
                    'bed_density': 2600,  # self.sed_properties("BedDensity"),
                    'organic_carbon_frac': 0.02,  # self.sed_properties("OrganicCarbonContent"),
                    'bed_pH': 7.3,  # self.sed_properties("pH"),
                    'bed_porosity': 0.6,  # self.sed_properties("Porosity"),
                    'bed_thickness': self.sed_properties("MeanThickness"),
                    'sed_burial_vol_rate': self.sed_burial_vol_rate,
                    'sed_deposition_vol_rate': self.sed_deposition_vol_rate,
                    'sed_resuspension_vel': self.sed_resuspension_vel,
                    'sed_soil_erosion_to_sw': self.sed_soil_erosion_to_sw
                }
            }
        }

    def calc_default_erosion_rate_sdr(self):
        for c in self.compartments:
            if c.name == "Soil_Surface":
                unit_soil_loss = c.parameters["unitSoilLoss"].default_value
                area_in_sq_mile = (self.area / 1E6) / 2.58998811
                if area_in_sq_mile <= 0.1:
                    intercept_coef = 2.1
                elif 0.1 < area_in_sq_mile <= 1:
                    intercept_coef = 1.9
                elif 1 < area_in_sq_mile <= 10:
                    intercept_coef = 1.4
                elif 10 < area_in_sq_mile <= 100:
                    intercept_coef = 1.2
                else:
                    intercept_coef = 0.6
                slope_coef = c.parameters["sedimentDeliveryRatioSlopeCoef"].default_value
                sed_delivery_ratio = intercept_coef * (self.area ** (-1 * slope_coef))
                return unit_soil_loss * sed_delivery_ratio

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.name}", area={self.area}'
            ')'
        )


class VolumeElement(Model):
    name = sa.Column(sa.String(120), nullable=False)

    parcel_id = sa.Column(
        sa.Integer(), sa.ForeignKey('parcel.id'), nullable=False
    )
    parcel = sa.orm.relationship(
        'Parcel', backref=sa.orm.backref('volume_elements', lazy='dynamic')
    )

    top = sa.Column(sa.Float(), nullable=False)
    bottom = sa.Column(sa.Float(), nullable=False)

    @property
    def standard_name(self):
        return f'{self.name}_{self.parcel.name}'

    @property
    def height(self):
        # CAREFUL: we assume dimensions are in meters ...
        return (self.top - self.bottom) * ureg('m')

    @property
    def depth(self):
        # CAREFUL: we assume dimensions are in meters ...
        return abs(self.top - self.bottom) * ureg('m')

    @property
    def volume(self):
        return self.parcel.area * self.height

    def agg(
        self, func, prop, chemical=None, compartment_name=None, compartment_media=None,
        *args, **kwargs
    ):
        comps = self.get_compartment(name=compartment_name, media=compartment_media)
        if not isinstance(comps, list):
            comps = [comps]

        def get_prop(c):
            if args or kwargs:
                if chemical is not None:
                    return getattr(chemical, prop)(c, *args, **kwargs)
                return getattr(c, prop)(*args, **kwargs)
            else:
                if chemical is not None:
                    return getattr(chemical, prop)(c)
                return getattr(c, prop)

        def eval_prop(c):
            p = get_prop(c)
            if isinstance(p, ParameterDefinition):
                return p.default_value
            elif isinstance(p, CustomParameter):
                return p.value
            else:
                return p

        if func == 'sum':
            props = []
            for c in comps:
                p = eval_prop(c)
                if pd.isna(p):
                    return pd.NA
                props.append(p)
            return sum(props)

        raise AssertionError('Unknown function!')

    def interface_with(self, volume_element):
        polygon_a = self.parcel.utm_polygon
        polygon_b = volume_element.parcel.utm_polygon

        is_neighbor = polygon_a.intersects(polygon_b)
        if not is_neighbor:
            # CAREFUL: we assume dimensions are in meters ...
            return 0 * ureg('m^3')  # technically m^2 ...

        intersection = polygon_a.intersection(polygon_b)

        if self.parcel.id == volume_element.parcel.id:  # polygon_a.almost_equals(polygon_b): # This is deprecated
            xy_overlap = self.parcel.area.magnitude  # This is in meters. We are good!
        else:
            xy_overlap = intersection.length  # TODO: This returns arc-degree units and not meter! Conversion needed!

        top_a = self.top
        top_b = volume_element.top

        bottom_a = self.bottom
        bottom_b = volume_element.bottom

        if (top_a == bottom_b or top_b == bottom_a) and intersection.area > 0:  # for overlying parcels:
            z_overlap = 1

        elif top_a >= top_b and top_b > bottom_a:
            z_overlap = top_b - bottom_a

        elif top_b >= top_a and top_a > bottom_b:
            z_overlap = top_a - bottom_b

        else:
            z_overlap = 0

        # CAREFUL: we assume dimensions are in meters ...
        return (z_overlap * xy_overlap) * ureg('m^3')  # technically m^2 ...

    def overlap_with(self, volume_element):
        if self.interface_with(volume_element) <= 0:
            return 0 * ureg('m^3')

        polygon_a = self.parcel.polygon
        polygon_b = volume_element.parcel.polygon

        is_neighbor = polygon_a.intersects(polygon_b)
        if not is_neighbor:
            # CAREFUL: we assume dimensions are in meters ...
            return 0 * ureg('m^3')

        intersection = polygon_a.intersection(polygon_b)
        xy_overlap = intersection.area

        top_a = self.top
        top_b = volume_element.top

        bottom_a = self.bottom
        bottom_b = volume_element.bottom

        if (top_a == bottom_b or top_b == bottom_a) and intersection.area > 0:  # for overlying parcels:
            # for overlying parcels
            z_overlap = 1

        elif top_a >= top_b and top_b > bottom_a:
            z_overlap = top_b - bottom_a

        elif top_b >= top_a and top_a > bottom_b:
            z_overlap = top_a - bottom_b

        else:
            z_overlap = 0

        # CAREFUL: we assume dimensions are in meters ...
        return (z_overlap * xy_overlap) * ureg('m^3')

    def midpoint_distance(self, volume_element):
        if isinstance(volume_element, Compartment):
            volume_element = volume_element.volume_element

        polygon_a = self.parcel.polygon
        polygon_b = volume_element.parcel.polygon

        # CAREFUL: we assume dimensions are in meters ...
        return polygon_a.centroid.distance(polygon_b.centroid) * ureg('m^2')


    def get_compartment(self, name=None, media=None):
        if name is None and media is None:
            raise ValueError('Must supply either "name" or "media" argument')
        if media is not None:
            check = [c for c in self.compartments if c.media.isa(media)]
            if name is None:
                return check
        else:
            check = self.compartments
        for x in check:
            if x.name == name or x.standard_name == name:
                return x
        return None

    # Each volume element should have a unique name relative to its parcel
    __table_args__ = (
        sa.UniqueConstraint('parcel_id', 'name'),
    )

    def as_serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'top': self.top,
            'bottom': self.bottom,
            'volume': self.volume
        }

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}("{self.standard_name}")'
        )


class Media(Model):
    name = sa.Column(sa.String(120), unique=True, nullable=False)

    parent_id = sa.Column(
        sa.Integer(),
        sa.ForeignKey('media.id'),
        nullable=True
    )
    parent = sa.orm.relationship(
        'Media',
        remote_side='Media.id',
        backref=sa.orm.backref('submedia', cascade='all, delete-orphan')
    )

    _can_emit = sa.Column(
        'can_emit', sa.Boolean(), nullable=False, default=True
    )
    _can_absorb = sa.Column(
        'can_absorb', sa.Boolean(), nullable=False, default=True
    )

    @property
    def can_emit(self):
        if self.parent is None:
            return self._can_emit
        return self._can_emit and self.parent.can_emit

    @can_emit.setter
    def can_emit(self, value):
        self._can_emit = value

    @property
    def can_absorb(self):
        if self.parent is None:
            return self._can_absorb
        return self._can_absorb and self.parent.can_absorb

    @can_absorb.setter
    def can_absorb(self, value):
        self._can_absorb = value

    @property
    def category(self):
        if self.parent is None:
            return self.name
        return f'{self.parent.category}|{self.name}'

    def isa(self, name_or_media):
        if isinstance(name_or_media, str):
            # check wildcard in the beginning
            if name_or_media.startswith(GLOBAL_WILDCARD):
                if (
                        self.name.endswith(name_or_media[1:])
                        or self.category.endswith(name_or_media[1:])
                ):
                    return True
            if name_or_media.endswith(GLOBAL_WILDCARD):
                if (
                        self.name.startswith(name_or_media[:-1])
                        or self.category.startswith(name_or_media[:-1])
                ):
                    return True
            else:
                if (
                    name_or_media == self.name
                    or name_or_media == self.category
                ):
                    return True
        elif isinstance(name_or_media, Media):
            if name_or_media.id == self.id:
                return True
        else:
            raise TypeError

        if self.parent is not None:
            return self.parent.isa(name_or_media)

        return False

    def as_serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category
        }

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.category}"'
            ')'
        )


class Compartment(Model):
    name = sa.Column(sa.String(120), nullable=False)

    volume_element_id = sa.Column(
        sa.Integer(), sa.ForeignKey('volume_element.id'), nullable=False
    )
    volume_element = sa.orm.relationship(
        'VolumeElement', backref=sa.orm.backref('compartments', lazy='dynamic')
    )

    media_id = sa.Column(
        sa.Integer(), sa.ForeignKey('media.id'), nullable=False
    )
    media = sa.orm.relationship(
        'Media', backref=sa.orm.backref('compartments', lazy='dynamic')
    )

    @property
    def standard_name(self):
        return f'{self.name} in {self.volume_element.standard_name}'

    @property
    def custom_linked_compartments(self):
        return [x.receiver for x in self._links]

    _linked_compartment_cache = {}

    def linked_compartments(self, media=None, same_parcel=False):
        # Check cache
        cache_k = f'{self.volume_element.parcel.name}--{media}--{same_parcel}'
        if cache_k in self._linked_compartment_cache:
            # This does not work if in a loop two parcels have generic media naming (i.e. $Leaf);
            # It gets compartments of the other parcel that was cached first. Berk turned this off...
            # return self._linked_compartment_cache[cache_k]
            self._linked_compartment_cache.clear()

        linked = {
            c.id: c for c in self.custom_linked_compartments
            if (media is None or c.media.isa(media))
        }
        linked.update({
            c.id: c for c in self.volume_element.parcel.compartments
            if (
                c != self and self.get_links(c)
                and (media is None or c.media.isa(media))
            )
        })

        linked = list(linked.values())

        # Set cache
        self._linked_compartment_cache[cache_k] = linked

        return linked

    def connects_to(self, compartment):
        if self.volume_element == compartment.volume_element:
            return True  # We're in the same "space"!

        elif self.volume_element.interface_with(compartment.volume_element) > 0:
            return True  # Our "spaces" touch!

        elif compartment in self.custom_linked_compartments:
            return True

        # To bad, we just didn't connect
        return False

    def is_next_to(self, compartment):
        if self.volume_element == compartment.volume_element:
            return False  # We're actually in the same "space" ...

        if self.volume_element.interface_with(compartment.volume_element) > 0:
            return True  # Our "spaces" touch!

        return False


    def get_links(self, compartment):
        comp_links = [
            x for x in self._links if x.receiver_id == compartment.id
        ]

        if len(comp_links):
            return comp_links

        if self.connects_to(compartment):
            comp_links.append(DummyLink(self, compartment))
        return comp_links

    # Each compartment should have a unique name in its volume element
    __table_args__ = (
        sa.UniqueConstraint('volume_element_id', 'name'),
    )

    def as_serializable(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        if self.name != self.media.category:
            return (
                f'{self.__class__.__qualname__}('
                f'"{self.standard_name}", "{self.media.category}"'
                ')'
            )
        else:
            return (
                f'{self.__class__.__qualname__}("{self.standard_name}")'
            )


class DummyLink:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.sender.standard_name}" > "{self.receiver.standard_name}"'
            ')'
        )


class CompartmentLink(Model):
    sender_id = sa.Column(
        sa.Integer(), sa.ForeignKey('compartment.id'), nullable=False
    )
    sender = sa.orm.relationship(
        'Compartment',
        foreign_keys=[sender_id],
        backref=sa.orm.backref('_links', lazy='dynamic')
    )

    receiver_id = sa.Column(
        sa.Integer(), sa.ForeignKey('compartment.id'), nullable=False
    )
    receiver = sa.orm.relationship(
        'Compartment',
        foreign_keys=[receiver_id]
    )

    # Each link should be unique
    __table_args__ = (
        sa.UniqueConstraint('sender_id', 'receiver_id'),
    )

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.sender.standard_name}" > "{self.receiver.standard_name}"'
            ')'
        )
