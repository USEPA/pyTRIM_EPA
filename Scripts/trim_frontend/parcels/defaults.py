from trim_db.schema import Parcel
from trim_db.schema.utils.serialize import register_serializer


@register_serializer(Parcel)
def serialize_parcel(pcl: Parcel):
    s = {
        'id': pcl.id,
        'name': pcl.name,
        'description': pcl.description,
        'vertices': pcl.vertices,
        'area': pcl.area.m_as('m^2'),

        'hasAir': pcl.has_air,
        'airDensity': pcl.air_density,
        'airHeight': pcl.air_height,
        'surfaceSoilThickness': pcl.surface_soil_height,
        'rootSoilThickness': pcl.root_soil_height,
        'vadoseSoilThickness': pcl.vadose_soil_height,
        "groundwaterZoneThickness": pcl.groundwater_height,
        'parcelType': pcl.parcel_type,
        'hasLand': pcl.has_land,
        'landUse': pcl.land_use,
        'hasFarmFoodChain': pcl.has_farm_food_chain,
        'hasFishFoodWeb': pcl.has_fish_food_web,
        'hasWetland': pcl.has_wetland,
        'dustLoad': pcl.dust_load,
        'dustDensity': pcl.dust_density,
        'fractionOrganicMatteronParticulates': pcl.fraction_organic_matter_on_particulates,
        'soilTillage': pcl.soil_tillage,
        'totalErosionRate': pcl.total_erosion_rate,
        'aquatic_diet_fractions': pcl.aquatic_diet_fractions,
        'aquatic_biomass': pcl.aquatic_property("BiomassPerArea"),
        'aquatic_bw': pcl.aquatic_property("BW"),
        'precip_rate': pcl.precipitation_rate,
        'precip_runoff_watershed_area': pcl.runoff_watershed_area,
        'precip_seepage_vol_rate_to_GW': pcl.seepage_vol_rate_to_gw,
        'precip_runoff_vol_rate_to_SW': pcl.runoff_vol_rate_to_sw,
        'precip_vol_rate_to_SW': pcl.precipitation_vol_rate_to_sw,
        'sed_soil_erosion_to_SW': pcl.sed_soil_erosion_to_sw,
        'surface_water': None if pcl.parcel_type not in ["Water Only", "Water & Air"] else {
            'wc_props':  {
                'flush_rate': 0.48,  # pcl.wc_properties("Flushes"),
                'suspended_sed_conc': 0.05,  # pcl.wc_properties("SuspendedSedimentConcentration"),
                'algae_density': 1.23E-2,  # pcl.wc_properties("AlgaeDensityInWaterColumn"),
                'chloride_conc': 7,  # pcl.wc_properties("ChlorideConcentration"),
                'chlorophyll_conc': 0.003,  # pcl.wc_properties("ChlorophyllConcentration"),
                'mean_depth': 3.6,  # pcl.wc_properties("MeanWaterDepth"),
                'evaporation_rate': 0.7,  # pcl.wc_properties("waterEvaporationRate"),
                'evaporation_vol_rate': pcl.evaporation_vol_rate,
                'suspended_organic_carbon': 0.05,  # pcl.wc_properties("OrganicCarbonContent"),
                'water_ph': 8.5,  # pcl.wc_properties("pH"),
                'sed_deposition_vel': 2,  # pcl.wc_properties("SedimentDepositionVelocity"),
                'water_temp': 286.15,  # pcl.wc_properties("WaterTemperature"),
                'sed_inflow': 0,  # pcl.wc_properties("ExternalSedimentInflow"),
                'discharge_vol_rate': pcl.wc_discharge_vol_rate,
                'sed_discharge_rate': pcl.wc_sed_discharge_rate
            },
            'sed_props': {
                'bed_density': 2600,  # pcl.sed_properties("BedDensity"),
                'organic_carbon_frac': 0.02,  # pcl.sed_properties("OrganicCarbonContent"),
                'bed_pH': 7.3,  # pcl.sed_properties("pH"),
                'bed_porosity': 0.6,  # pcl.sed_properties("Porosity"),
                'bed_thickness': pcl.sed_properties("MeanThickness"),
                'sed_burial_vol_rate': pcl.sed_burial_vol_rate,
                'sed_deposition_vol_rate': pcl.sed_deposition_vol_rate,
                'sed_resuspension_vel': pcl.sed_resuspension_vel,
                'sed_soil_erosion_to_sw': pcl.sed_soil_erosion_to_sw
            }
        }
    }
    return s


Wet_Dry_Source_VolElem_defaults = {
    'DryParticleSource': {
        'name': 'DryParticleSource',
        'top': -3.65,
        'bottom': -11.65,
        'Compartments': {
            'DryParticleSource': {
                'name': 'DryParticleSource',
                'media_name': 'Particle'
            }
        }
    },
    'DryVaporSource': {
        'name': 'DryVaporSource',
        'top': -11.65,
        'bottom': -19.65,
        'Compartments': {
            'DryVaporSource': {
                'name': 'DryVaporSource',
                'media_name': 'Vapor'
            }
        }
    },
    'WetParticleSource': {
        'name': 'WetParticleSource',
        'top': -19.65,
        'bottom': -27.65,
        'Compartments': {
            'WetParticleSource': {
                'name': 'WetParticleSource',
                'media_name': 'Particle'
            }
        }
    },
    'WetVaporSource': {
        'name': 'WetVaporSource',
        'top': -27.65,
        'bottom': -35.65,
        'Compartments': {
            'WetVaporSource': {
                'name': 'WetVaporSource',
                'media_name': 'Vapor'
            }
        }
    }
}

Aquatic_Biota_Sed_Compartment_defaults = {
    'Compartments': {
        'Benthic_Carnivore': {
            'name': 'Benthic_Carnivore',
            'media_name': 'Benthic_Carnivore'
        },
        'Benthic_Invertebrate': {
            'name': 'Benthic_Invertebrate',
            'media_name': 'Benthic_Invertebrate'
        },
        'Benthic_Omnivore': {
            'name': 'Benthic_Omnivore',
            'media_name': 'Benthic_Omnivore'
        }
    }
}

Aquatic_Biota_SW_Compartment_defaults = {
    'Compartments': {
        'Macrophyte': {
            'name': 'Macrophyte',
            'media_name': 'Macrophyte'
        },
        'Water_Column_Carnivore': {
            'name': 'Water_Column_Carnivore',
            'media_name': 'Water_Column_Carnivore'
        },
        'Water_Column_Herbivore': {
            'name': 'Water_Column_Herbivore',
            'media_name': 'Water_Column_Herbivore'
        },
        'Water_Column_Omnivore': {
            'name': 'Water_Column_Omnivore',
            'media_name': 'Water_Column_Omnivore'
        },
        'Zooplankton': {
            'name': 'Zooplankton',
            'media_name': 'Plankton'
        }
    }
}

Air_Parcel_VolElem_defaults = {
    'Air': {
        'name': 'Air',
        'top': 800,
        'bottom': 0,
        'Compartments': {
            'Air': {
                'name': 'Air',
                'media_id': 2,
                'media_name': 'Air'
            },
            'Degradation_Reaction_Sink': {
                'name': 'Degradation_Reaction_Sink',
                'media_id': 15,
                'media_name': 'Degradation_Reaction'
            }
        }
    },
    'UpperAir': {
        'name': 'UpperAir',
        'top': 1000,
        'bottom': 800,
        'Compartments': {
            'Air': {
                'name': 'Air',
                'media_id': 2,
                'media_name': 'Air'
            }
        }
    }
}

Land_Parcel_VolElem_defaults = {
    'SurfSoil': {
        'name': 'SurfSoil',
        'top': 0,
        'bottom': -0.01,
        'Compartments': {
            'Soil_Surface': {
                'name': 'Soil_Surface',
                'media_id': 7,
                'media_name': 'Surface_Soil'
            },
            'Degradation_Reaction_Sink': {
                'name': 'Degradation_Reaction_Sink',
                'media_id': 15,
                'media_name': 'Degradation_Reaction'
            },
            'Leaf_Grasses_Herbs': {
                'name': 'Leaf_Grasses_Herbs',
                'media_id': 40,
                'media_name': 'Grass_Leaf'
            },
            'Leaf_Particle_Grasses_Herbs': {
                'name': 'Leaf_Particle_Grasses_Herbs',
                'media_id': 44,
                'media_name': 'Grass_Leaf_Particle'
            },
            'Stem_Grasses_Herbs': {
                'name': 'Stem_Grasses_Herbs',
                'media_id': 42,
                'media_name': 'Grass_Stem'
            },
            'Root_Grasses_Herbs': {
                'name': 'Root_Grasses_Herbs',
                'media_id': 45,
                'media_name': 'Grass_Root'
            },
        }
    }
}

Water_Parcel_VolElem_defaults = {
    'SW': {
        'name': 'SW',
        'top': 0,
        'bottom': -3.6,
        'Compartments': {
            'Surface_water': {
                'name': 'Surface_water',
                'media_id': 4,
                'media_name': 'Surface_Water'
            },
            'Degradation_Reaction_Sink': {
                'name': 'Degradation_Reaction_Sink',
                'media_id': 15,
                'media_name': 'Degradation_Reaction'
            },
            'Flush_Rate_Sink': {
                'name': 'Flush_Rate_Sink',
                'media_id': 18,
                'media_name': 'Flush_Rate'
            }
        }
    },
    'Sed': {
        'name': 'Sed',
        'top': -3.6,
        'bottom': -3.65,
        'Compartments': {
            'Sediment': {
                'name': 'Sediment',
                'media_id': 5,
                'media_name': 'Sediment'
            },
            'Degradation_Reaction_Sink': {
                'name': 'Degradation_Reaction_Sink',
                'media_id': 15,
                'media_name': 'Degradation_Reaction'
            },
        }
    }
}
