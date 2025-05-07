# CHEMICAL general porting rules

CHEMICAL_PROPS_DONT_TRANSFER = [
    'CAS', 'enabled'
]


# MEDIA general porting rules

MEDIA_MAP = {
    'Air': (
        'Abiotic|Air'
    ),
    'Sediment': (
        'Abiotic|Sediment'
    ),
    'Surface_water': (
        'Abiotic|Water|Surface_Water'
    ),
    'Groundwater': (
        'Abiotic|Water|Groundwater'
    ),
    'Soil_Surface': (
        'Abiotic|Soil|Surface_Soil'
    ),
    'Surface_Soil': (
        'Abiotic|Soil|Surface_Soil'
    ),
    'Surface_Soil_Default': (
        'Abiotic|Soil|Surface_Soil'
    ),
    'Root_Zone': (
        'Abiotic|Soil|Root_Zone'
    ),
    'Soil_Root_Zone': (
        'Abiotic|Soil|Root_Zone'
    ),
    'Vadose_zone': (
        'Abiotic|Soil|Vadose_Zone'
    ),
    'Soil_Vadose_Zone': (
        'Abiotic|Soil|Vadose_Zone'
    ),
    'Source': (
        'Source'
    ),
    'DryVaporSource': (
        'Source|Vapor|Dry_Vapor'
    ),
    'WetVaporSource': (
        'Source|Vapor|Wet_Vapor'
    ),
    'DryParticleSource': (
        'Source|Particle|Dry_Particle'
    ),
    'WetParticleSource': (
        'Source|Particle|Wet_Particle'
    ),
    'Soil_Sink': (
        'Sink|Abiotic_Sink|Soil_Sink'
    ),
    'Soil_Advection_Sink': (
        'Sink|Abiotic_Sink|Advection'
    ),
    'Air_Advection_Sink': (
        'Sink|Abiotic_Sink|Advection'
    ),
    'Flush_Rate_Sink': (
        'Sink|Abiotic_Sink|Advection|Flush_Rate'
    ),
    'Burial_Sink': (
        'Sink|Abiotic_Sink|Burial'
    ),
    'Degradation_Reaction_Sink': (
        'Sink|Degradation_Reaction'
    ),
    'Fish': (
        'Biotic|Aquatic|Fish'
    ),
    'Macrophyte': (
        'Biotic|Aquatic|Macrophyte'
    ),
    'Zooplankton': (
        'Biotic|Aquatic|Plankton'
    ),
    'Water_Column_Herbivore': (
        'Biotic|Aquatic|Fish|Water_Column|Water_Column_Herbivore'
    ),
    'Water_Column_Omnivore': (
        'Biotic|Aquatic|Fish|Water_Column|Water_Column_Omnivore'
    ),
    'Water_Column_Carnivore': (
        'Biotic|Aquatic|Fish|Water_Column|Water_Column_Carnivore'
    ),
    'Benthic_Invertebrate': (
        'Biotic|Aquatic|Fish|Benthic|Benthic_Invertebrate'
    ),
    'Benthic_Omnivore': (
        'Biotic|Aquatic|Fish|Benthic|Benthic_Omnivore'
    ),
    'Benthic_Carnivore': (
        'Biotic|Aquatic|Fish|Benthic|Benthic_Carnivore'
    ),
    'Leaf_Agriculture_General': (
        'Biotic|Terrestrial|Flora|Agriculture|Agriculture_Leaf'
    ),
    'Leaf_Particle_Agriculture_General': (
        'Biotic|Terrestrial|Flora|Agriculture|Agriculture_Leaf_Particle'
    ),
    'Stem_Agriculture_General': (
        'Biotic|Terrestrial|Flora|Agriculture|Agriculture_Stem'
    ),
    'Root_Agriculture_General': (
        'Biotic|Terrestrial|Flora|Agriculture|Agriculture_Root'
    ),
    'Leaf_Coniferous_Forest': (
        'Biotic|Terrestrial|Flora|Coniferous_Forest|Coniferous_Leaf'
    ),
    'Leaf_Particle_Coniferous_Forest': (
        'Biotic|Terrestrial|Flora|Coniferous_Forest|Coniferous_Leaf_Particle'
    ),
    'Leaf_Deciduous_Forest': (
        'Biotic|Terrestrial|Flora|Deciduous_Forest|Deciduous_Leaf'
    ),
    'Leaf_Particle_Deciduous_Forest': (
        'Biotic|Terrestrial|Flora|Deciduous_Forest|Deciduous_Leaf_Particle'
    ),
    'Leaf_Grasses_Herbs': (
        'Biotic|Terrestrial|Flora|Grass|Grass_Leaf'
    ),
    'Leaf_Particle_Grasses_Herbs': (
        'Biotic|Terrestrial|Flora|Grass|Grass_Leaf_Particle'
    ),
    'Stem_Grasses_Herbs': (
        'Biotic|Terrestrial|Flora|Grass|Grass_Stem'
    ),
    'Root_Grasses_Herbs': (
        'Biotic|Terrestrial|Flora|Grass|Grass_Root'
    )
}
for k, v in list(MEDIA_MAP.items()):
    for pref in sorted(['Leaf_', 'Leaf_Particle_', 'Root_', 'Stem_'], key=len):
        if not k.startswith(pref):
            continue
        variant = f'{k}_in_{k[len(pref):]}'
        if variant not in MEDIA_MAP:
            MEDIA_MAP[variant] = v
