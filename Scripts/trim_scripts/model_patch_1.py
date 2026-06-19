from sqlalchemy.exc import IntegrityError
from datetime import datetime as dt

from base import *

# FIX Wrongly parsed formulas
FORMULA_REPLACE = {
    " min (": " min(",
    "SedimentPartitioning_TimetoReachAlphaofEquilibrium": "SedimentPartitioning_TimeToReachAlphaofEquilibrium",
    ".Conc_colloid ": ".conc_Colloid "
}

CHEMS_TO_ADD = [
    # Dioxins
    # "1,2,3,4,6,7,8,9-OCDD",
    # "1,2,3,4,6,7,8,9-OCDF",
    # "1,2,3,4,6,7,8-HpCDD",
    # "1,2,3,4,6,7,8-HpCDF",
    # "1,2,3,4,7,8,9-HpCDF",
    # "1,2,3,4,7,8-HxCDD",
    # "1,2,3,4,7,8-HxCDF",
    # "1,2,3,6,7,8-HxCDD",
    # "1,2,3,6,7,8-HxCDF",
    # "1,2,3,7,8,9-HxCDD",
    # "1,2,3,7,8,9-HxCDF",
    # "1,2,3,7,8-PeCDD",
    # "1,2,3,7,8-PeCDF",
    # "2,3,4,6,7,8-HxCDF",
    # "2,3,4,7,8-PeCDF",
    # "2,3,7,8-TCDF",

    # PAHs
    "2-Methylnaphthalene",
    "7,12-Dimethylbenz(a)anthracene",
    "Acenaphthene",
    "Acenaphthylene",

    "Benz(a)anthracene",
    "Benzo(b)fluoranthene",
    "Benzo(g,h,i)perylene",
    "Benzo(k)fluoranthene",

    "Chrysene",
    "Dibenz(a,h)anthracene",
    "Fluoranthene",
    "Fluorene",
    "Indeno(1,2,3-cd)pyrene"
]

# FIX ALGORITHM PROBLEMS
ALG_UPDATES =[{
        'shn': 'dry vapor to soil, Hg0',
        'name': 'Diffusion from DryVaporSource to Surface Soil, Hg0',
        'type': 'Transport|Abstract transfer',
        'reqs': '(chemical.id == 32) and (sender.media.isa("Source|Dry_Vapor")) and (receiver.media.isa("Abiotic|Soil|Surface_Soil"))',
        'eqn': 'receiver.TransferFactorToSoilNonConiferousLeaf(chemical) if receiver.return_sameparcel_linked_media_id_or_none(media="$Leaf") in {37 , 41 , 43} else receiver.TransferFactorToSoilConiferousLeaf(chemical) if receiver.return_sameparcel_linked_media_id_or_none(media="$Leaf") in {39} else 1'
    },
    {
        'shn': 'dry vapor to plant, Hg0',
        'name': 'Diffusion from DryVaporSource to Plant Leaf, Hg0',
        'type': 'Transport|Abstract transfer',
        'reqs': '(chemical.id == 32) and (sender.media.isa("Source|Dry_Vapor")) and (receiver.media.isa("Biotic|Terrestrial|Flora|Agriculture|Agriculture_Leaf") or receiver.media.isa("Biotic|Terrestrial|Flora|Coniferous_Forest|Coniferous_Leaf") or receiver.media.isa("Biotic|Terrestrial|Flora|Deciduous_Forest|Deciduous_Leaf") or receiver.media.isa("Biotic|Terrestrial|Flora|Grass|Grass_Leaf") or receiver.media.isa("Biotic|Terrestrial|Flora|Agriculture|Agriculture_Leaf") or receiver.media.isa("Biotic|Terrestrial|Flora|Coniferous_Forest|Coniferous_Leaf") or receiver.media.isa("Biotic|Terrestrial|Flora|Deciduous_Forest|Deciduous_Leaf") or receiver.media.isa("Biotic|Terrestrial|Flora|Grass|Grass_Leaf"))',
        'eqn': 'receiver.TransferFactorToLeafNonConiferousLeaf(chemical) if receiver.media.id in {37 , 41 , 43} else receiver.TransferFactorToLeafConiferousLeaf(chemical) if receiver.media.id in {39} else 0'
    }]

# ADD Missing Pseudo-Source Algorithms
PS_ALGS = [
    {
        'shn': 'wet vapor to soil',
        'name': 'Wet Deposition of Vapor Phase from WetVaporSource to Soil, Organics',
        'type': 'Transport|Abstract transfer',
        'reqs': '(chemical.isa("Organic")) and (sender.media.isa("Source|Wet_Vapor")) and (receiver.media.isa("Abiotic|Soil|Surface_Soil"))',
        'eqn': '1 - (receiver.volume_element.agg("sum" , "AllowExchange_forAir" , compartment_media="$Leaf") * receiver.volume_element.agg("sum" , "WetDepInterceptionFraction" , compartment_media="$Leaf"))'
    },
    {
        'shn': 'dry vapor to soil',
        'name': 'Diffusion from DryVaporSource to Surface Soil, Organics',
        'type': 'Transport|Abstract transfer',
        'reqs': '(chemical.isa("Organic")) and (sender.media.isa("Source|Dry_Vapor")) and (receiver.media.isa("Abiotic|Soil|Surface_Soil"))',
        'eqn': 'receiver.TransferFactorToSoilNonConiferousLeaf(chemical) if receiver.return_sameparcel_linked_media_id_or_none(media="$Leaf") in {37 , 41 , 43} else receiver.TransferFactorToSoilConiferousLeaf(chemical) if receiver.return_sameparcel_linked_media_id_or_none(media="$Leaf") in {39} else 1'
    },
    {
        'shn': 'dry vapor to plant',
        'name': 'Diffusion from DryVaporSource to Plant Leaf, Organics',
        'type': 'Transport|Abstract transfer',
        'reqs': '(chemical.isa("Organic")) and (sender.media.isa("Source|Dry_Vapor")) and (receiver.media.isa("Biotic|Terrestrial|Flora|Agriculture|Agriculture_Leaf") or receiver.media.isa("Biotic|Terrestrial|Flora|Coniferous_Forest|Coniferous_Leaf") or receiver.media.isa("Biotic|Terrestrial|Flora|Deciduous_Forest|Deciduous_Leaf") or receiver.media.isa("Biotic|Terrestrial|Flora|Grass|Grass_Leaf"))',
        'eqn': 'receiver.TransferFactorToLeafNonConiferousLeaf(chemical) if receiver.media.id in {37 , 41 , 43} else receiver.TransferFactorToLeafConiferousLeaf(chemical) if receiver.media.id in {39} else 0'
    }
    ]

PS_ALG_PARS = [
    {
        'name': 'TransferFractionToLeafNonConiferousLeaf_AE_not_day',
        'formula': '(self.volume_element.parcel.area * 2 * self.LeafAreaIndex * chemical.TotalCuticularConductance(self))',
        'unit': 'm^3/day',
        'domain_ids': [15, 17, 18]
    },
    {
        'name': 'TransferFractionToLeafNonConiferousLeaf_AE_day',
        'formula': 'self.TransferFractionToLeafNonConiferousLeaf_AE_not_day(chemical)' +
                  ' + (self.volume_element.parcel.area * self.LeafAreaIndex * chemical.TotalStomatalConductance(self))',
        'unit': 'm^3/day',
        'domain_ids': [15, 17, 18]
    },
    {
        'name': 'TransferFractionToLeafNonConiferousLeaf_no_AE',
        'value': 0,
        'unit': 'm^3/day',
        'domain_ids': [15, 17, 18]
    },
    {
        'name': 'TransferFractionToLeafConiferousLeaf',
        'formula': '(self.AllowExchange_forAir * (self.volume_element.parcel.area * 2 * self.LeafAreaIndex * chemical.TotalCuticularConductance(self)) + (self.LeafAreaIndex * self.volume_element.parcel.area * (self.isDay_forAir * chemical.TotalStomatalConductance(self))))',
        'unit': 'm^3/day',
        'domain_ids': [16]
    },
    {
        'name': 'TransferFractionToLeafSoil',
        'formula': '(((self.volume_element.agg("sum" , "FractionofAreaAvailableforVerticalDiffusion" , compartment_media="Abiotic|Soil|Surface_Soil") * self.volume_element.parcel.area) / chemical.Z_PureAir) * ((1 / (chemical.Z_PureAir * (self.volume_element.agg("sum" , "MassTransferCoefficientOnAirSideofAirSoilBoundary" , chemical=chemical , compartment_media="Abiotic|Soil|Surface_Soil")))) + (1 / (self.volume_element.agg("sum" , "Z_Total" , chemical=chemical , compartment_media="Abiotic|Soil|Surface_Soil") * (self.volume_element.agg("sum" , "D_effective" , chemical=chemical , compartment_media="Abiotic|Soil|Surface_Soil") / self.volume_element.depth)))) ** (- 1))',
        'unit': 'm^3/day',
        'domain_ids': [15, 16, 17, 18]
    },
    {
        'name': 'TransferFractionToLeafTotalNonConiferousLeaf_AE_not_day',
        'formula': 'self.TransferFractionToLeafNonConiferousLeaf_AE_not_day(chemical) + self.TransferFractionToLeafSoil(chemical)',
        'unit': 'm^3/day',
        'domain_ids': [15, 17, 18]
    },
    {
        'name': 'TransferFractionToLeafTotalNonConiferousLeaf_AE_day',
        'formula': 'self.TransferFractionToLeafNonConiferousLeaf_AE_day(chemical) + self.TransferFractionToLeafSoil(chemical)',
        'unit': 'm^3/day',
        'domain_ids': [15, 17, 18]
    },
    {
        'name': 'TransferFractionToLeafTotalNonConiferousLeaf_no_AE',
        'formula': 'self.TransferFractionToLeafNonConiferousLeaf_no_AE + self.TransferFractionToLeafSoil(chemical)',
        'unit': 'm^3/day',
        'domain_ids': [15, 17, 18]
    },
    {
        'name': 'TransferFractionToLeafTotalConiferousLeaf',
        'formula': 'self.TransferFractionToLeafConiferousLeaf(chemical) + self.TransferFractionToLeafSoil(chemical)',
        'unit': 'm^3/day',
        'domain_ids': [16]
    },
    {
        'name': 'TransferFactorToLeafNonConiferousLeaf_LeafComponent',
        'formula': '(((1-self.isDay_forAir) * self.AllowExchange_forAir) * self.TransferFractionToLeafNonConiferousLeaf_AE_not_day(chemical) / self.TransferFractionToLeafTotalNonConiferousLeaf_AE_not_day(chemical)) + ((self.isDay_forAir * self.AllowExchange_forAir)* self.TransferFractionToLeafNonConiferousLeaf_AE_day(chemical) / self.TransferFractionToLeafTotalNonConiferousLeaf_AE_day(chemical)) + ((1 - self.AllowExchange_forAir) * self.TransferFractionToLeafNonConiferousLeaf_no_AE / self.TransferFractionToLeafTotalNonConiferousLeaf_no_AE(chemical))',
        'unit': None,
        'domain_ids': [15, 17, 18]
    },
    {
        'name': 'TransferFactorToLeafNonConiferousLeaf_SoilComponent',
        'formula': '(((1-self.isDay_forAir) *self.AllowExchange_forAir) * self.TransferFractionToLeafSoil(chemical) / self.TransferFractionToLeafTotalNonConiferousLeaf_AE_not_day(chemical)) + (self.isDay_forAir * self.AllowExchange_forAir * self.TransferFractionToLeafSoil(chemical)/ self.TransferFractionToLeafTotalNonConiferousLeaf_AE_day(chemical)) + ((1 - self.AllowExchange_forAir) * self.TransferFractionToLeafSoil(chemical) / self.TransferFractionToLeafTotalNonConiferousLeaf_no_AE(chemical))',
        'unit': None,
        'domain_ids': [15, 17, 18]
    },
    {
        'name': 'TransferFactorToLeafNonConiferousLeaf',
        'formula': 'self.TransferFactorToLeafNonConiferousLeaf_LeafComponent(chemical) / (self.TransferFactorToLeafNonConiferousLeaf_LeafComponent(chemical) + self.TransferFactorToLeafNonConiferousLeaf_SoilComponent(chemical))',
        'unit': None,
        'domain_ids': [15, 17, 18]
    },
    {
        'name': 'TransferFactorToLeafConiferousLeaf',
        'formula': '(self.TransferFractionToLeafConiferousLeaf(chemical) / self.TransferFractionToLeafTotalConiferousLeaf(chemical)) if self.TransferFractionToLeafTotalConiferousLeaf(chemical) > 0 else 0',
        'unit': None,
        'domain_ids': [16]
    },
    {
        'name': 'TransferFractionToSoilNonConiferousLeaf_AE_not_day',
        'formula': '(self.volume_element.parcel.area * 2 * self.volume_element.agg("sum" , "LeafAreaIndex" , compartment_media="$Leaf") * self.volume_element.agg("sum" , "TotalCuticularConductance" , chemical=chemical , compartment_media="$Leaf"))',
        'unit': 'm^3/day',
        'domain_ids': [28, 39, 40]
    },
    {
        'name': 'TransferFractionToSoilNonConiferousLeaf_AE_day',
        'formula': 'self.TransferFractionToSoilNonConiferousLeaf_AE_not_day(chemical)' +
                   ' + (self.volume_element.parcel.area * self.volume_element.agg("sum" , "LeafAreaIndex" , compartment_media="$Leaf") * self.volume_element.agg("sum" , "TotalStomatalConductance" , chemical=chemical , compartment_media="$Leaf"))',
        'unit': 'm^3/day',
        'domain_ids': [28, 39, 40]
    },
    {
        'name': 'TransferFractionToSoilNonConiferousLeaf_no_AE',
        'value': 0,
        'unit': 'm^3/day',
        'domain_ids': [28, 39, 40]
    },
    {
        'name': 'TransferFractionToSoilConiferousLeaf',
        'formula': '(self.volume_element.agg("sum" , "AllowExchange_forAir" , compartment_media="$Leaf") * (self.volume_element.parcel.area * 2 * self.volume_element.agg("sum" , "LeafAreaIndex" , compartment_media="$Leaf") * self.volume_element.agg("sum" , "TotalCuticularConductance" , chemical=chemical , compartment_media="$Leaf")) + (self.volume_element.parcel.area * self.volume_element.agg("sum" , "LeafAreaIndex" , compartment_media="$Leaf") * (self.volume_element.agg("sum" , "isDay_forAir" , compartment_media="$Leaf") * self.volume_element.agg("sum" , "TotalStomatalConductance" , chemical=chemical , compartment_media="$Leaf"))))',
        'unit': 'm^3/day',
        'domain_ids': [28, 39, 40]
    },
    {
        'name': 'TransferFractionToSoilSoil',
        'formula': '(((self.FractionofAreaAvailableforVerticalDiffusion * self.volume_element.parcel.area) / chemical.Z_PureAir) * ((1 / (chemical.Z_PureAir * (chemical.MassTransferCoefficientOnAirSideofAirSoilBoundary(self)))) + (1 / (chemical.Z_Total(self) * (chemical.D_effective(self) / self.volume_element.depth)))) ** (- 1))',
        'unit': 'm^3/day',
        'domain_ids': [28, 39, 40]
    },
    {
        'name': 'TransferFractionToSoilTotalNonConiferousLeaf_AE_not_day',
        'formula': 'self.TransferFractionToSoilNonConiferousLeaf_AE_not_day(chemical) + self.TransferFractionToSoilSoil(chemical)',
        'unit': 'm^3/day',
        'domain_ids': [28, 39, 40]
    },
    {
        'name': 'TransferFractionToSoilTotalNonConiferousLeaf_AE_day',
        'formula': 'self.TransferFractionToSoilNonConiferousLeaf_AE_day(chemical) + self.TransferFractionToSoilSoil(chemical)',
        'unit': 'm^3/day',
        'domain_ids': [28, 39, 40]
    },
    {
        'name': 'TransferFractionToSoilTotalNonConiferousLeaf_no_AE',
        'formula': 'self.TransferFractionToSoilNonConiferousLeaf_no_AE + self.TransferFractionToSoilSoil(chemical)',
        'unit': 'm^3/day',
        'domain_ids': [28, 39, 40]
    },
    {
        'name': 'TransferFractionToSoilTotalConiferousLeaf',
        'formula': 'self.TransferFractionToSoilConiferousLeaf(chemical) + self.TransferFractionToSoilSoil(chemical)',
        'unit': 'm^3/day',
        'domain_ids': [28, 39, 40]
    },
    {
        'name': 'TransferFactorToSoilNonConiferousLeaf_LeafComponent',
        'formula': '((1-self.volume_element.agg("sum" , "isDay_forAir" , compartment_media="$Leaf")) * self.volume_element.agg("sum" , "AllowExchange_forAir" , compartment_media="$Leaf") * self.TransferFractionToSoilNonConiferousLeaf_AE_not_day(chemical) / self.TransferFractionToSoilTotalNonConiferousLeaf_AE_not_day(chemical)) + (self.volume_element.agg("sum" , "isDay_forAir" , compartment_media="$Leaf") * self.volume_element.agg("sum" , "AllowExchange_forAir" , compartment_media="$Leaf") * self.TransferFractionToSoilNonConiferousLeaf_AE_day(chemical) / self.TransferFractionToSoilTotalNonConiferousLeaf_AE_day(chemical)) + ((1 - self.volume_element.agg("sum" , "AllowExchange_forAir" , compartment_media="$Leaf")) * self.TransferFractionToSoilNonConiferousLeaf_no_AE / self.TransferFractionToSoilTotalNonConiferousLeaf_no_AE(chemical))',
        'unit': None,
        'domain_ids': [28, 39, 40]
    },
    {
        'name': 'TransferFactorToSoilNonConiferousLeaf_SoilComponent',
        'formula': '((1-self.volume_element.agg("sum" , "isDay_forAir" , compartment_media="$Leaf")) * self.volume_element.agg("sum" , "AllowExchange_forAir" , compartment_media="$Leaf") * self.TransferFractionToSoilSoil(chemical) / self.TransferFractionToSoilTotalNonConiferousLeaf_AE_not_day(chemical)) + (self.volume_element.agg("sum" , "isDay_forAir" , compartment_media="$Leaf") * self.volume_element.agg("sum" , "AllowExchange_forAir" , compartment_media="$Leaf") * self.TransferFractionToSoilSoil(chemical) / self.TransferFractionToSoilTotalNonConiferousLeaf_AE_day(chemical)) + ((1 - self.volume_element.agg("sum" , "AllowExchange_forAir" , compartment_media="$Leaf")) * self.TransferFractionToSoilSoil(chemical) / self.TransferFractionToSoilTotalNonConiferousLeaf_no_AE(chemical))',
        'unit': None,
        'domain_ids': [28, 39, 40]
    },
    {
        'name': 'TransferFactorToSoilNonConiferousLeaf',
        'formula': 'self.TransferFactorToSoilNonConiferousLeaf_SoilComponent(chemical) / (self.TransferFactorToSoilNonConiferousLeaf_LeafComponent(chemical) + self.TransferFactorToSoilNonConiferousLeaf_SoilComponent(chemical))',
        'unit': None,
        'domain_ids': [28, 39, 40]
    },
    {
        'name': 'TransferFactorToSoilConiferousLeaf',
        'formula': '(self.TransferFractionToSoilSoil(chemical) / self.TransferFractionToSoilTotalConiferousLeaf(chemical)) if self.TransferFractionToSoilTotalConiferousLeaf(chemical) > 0 else 0',
        'unit': None,
        'domain_ids': [28, 39, 40]
    },
]

# FIX WRONG UNITS
# FIX Cuticular conductance unit [should be changed from m/sec to m/day]
UNIT_FIXES = {
    'CuticularConductance': 'm/day'
}

# FIX CONIFEROUS LEAF/LEAF-PARTICLE ALLOW_EXCHANGE AND OTHER PARAMETER FORMULAS THAT ARE SPECIFIC TO ANY DOMAIN...
DOMAIN_SPECIFIC_PARAM_FORMULA_REPLACEMENTS = [
    {
        'variable_name': "AllowExchange_forOther",
        'domain': 'Compartment [Coniferous_Leaf]',
        'old_formula': "self.AllowExchange_SteadyState_forOther if environment.simulateSteadyState == 1 else self.AllowExchange_Dynamic",
        'new_formula': "self.AllowExchange_SteadyState_forOther if environment.simulateSteadyState == 1 else 1"
    },
    {
        'variable_name': "AllowExchange_forOther",
        'domain': 'Compartment [Coniferous_Leaf_Particle]',
        'old_formula': "self.AllowExchange_SteadyState_forOther if environment.simulateSteadyState == 1 else self.AllowExchange_Dynamic",
        'new_formula': "self.AllowExchange_SteadyState_forOther if environment.simulateSteadyState == 1 else 1"
    },
    {
        'variable_name': "AllowExchange_forAir",
        'domain': 'Compartment [Coniferous_Leaf]',
        'old_formula': "self.AllowExchange_SteadyState_forAir if environment.simulateSteadyState == 1 else self.AllowExchange_Dynamic",
        'new_formula': "self.AllowExchange_SteadyState_forAir if environment.simulateSteadyState == 1 else 1"
    },
]

# FIX Missing links for Tier1_Hg_* scenarios
SCENARIO_NAMES = ['Tier1_TCDD', 'Tier1_Hg', 'Tier1_Hg_V#1', 'Tier1_Hg_w_Background', 'Tier1_BaP', 'Tier1_Cd']
ORIG_SCENARIO_NAME = 'Tier1_Hg'

# ADD MISSING PARAMETER DEFINITIONS
NEW_PARAMETER_DEFS = [
    {'variable_name': 'Volume',
     'full_name': 'Volume',
     'domain_id': ParameterService.domains.get(name="Compartment [Macrophyte]").id,
     'default_unit': "m^3",
     'default_value': None,
     'default_formula': "self.TotalMass / (self.Density * 1000)"
     },
    {
     'variable_name': 'mixingHeight',
     'full_name': 'mixingHeight',
     'domain_id': ParameterService.domains.get(name="Scenario").id,
     'default_unit': "m",
     'default_value': 226,
     'default_formula': None
    }
]

# UPDATE PARAMETERS
UPDATE_PARS = [
    {'variable_name': 'rho',
     'domain_id': 33,
     'default_value': 2600,
     },
 ]

# DELETE WRONG COMPARTMENT SPECIFIC CUSTOM PARAMETERS
CUSTOM_PARS_TO_DELETE = [
    {'par_name': 'LitterFallRate',
     'comp_media': 'Coniferous_Leaf'}
]

def fix_custom_links():
    # DO CUSTOM LINK FIX
    scenario_orig = ScenarioService.get(name=ORIG_SCENARIO_NAME)
    for SCENARIO_NAME in SCENARIO_NAMES:
        loggy(f"Fixing Custom links in {SCENARIO_NAME}...")
        scenario_1 = ScenarioService.get(name=SCENARIO_NAME)

        ll = {c.standard_name: {'sender': c,
                                'receiver': c.custom_linked_compartments,
                                'clinks': [
                                    CompartmentService.links.get(sender_id=c.id, receiver_id=cc.id) for cc in c.custom_linked_compartments
                                ]
                                } for c in scenario_orig.compartments if len(c.custom_linked_compartments) > 0}

        for l, ld in ll.items():
            sender_1 = [c for c in scenario_1.compartments if c.standard_name == l][0]
            for r1 in ld['receiver']:
                receiver_1 = [c for c in scenario_1.compartments if c.standard_name == r1.standard_name][0]
                ccl = CompartmentService.links.get(sender_id=sender_1.id, receiver_id=receiver_1.id)
                if not ccl:
                    print(f'CREATING A NEW LINK in SCENARIO {receiver_1.volume_element.parcel.scenario.name} with sender_id:{sender_1.id} and receiver_id {receiver_1.id}')
                    CompartmentService.links.create(sender_id=sender_1.id, receiver_id=receiver_1.id)
                else:
                    print(
                        f'A CUSTOM LINK ALREADY EXISTS in SCENARIO {receiver_1.volume_element.parcel.scenario.name} with sender_id:{sender_1.id} and receiver_id {receiver_1.id}')
            CompartmentService.commit()


def run_chem_migrations(ch, mode="check"):
    # RUN CHEMICAL PROPERTY MIGRATIONS
    loggy(f"Importing chem params for {ch} now ...")
    import_script = os.path.join(Path(__file__).parent.resolve(), "import_new_chemicals.py")
    os.system(f"python {import_script} --runtype={mode} --chemical={ch}")


def do_formula_replacements():
    # DO THE FORMULA REPLACEMENTS
    for old, new in FORMULA_REPLACE.items():
        loggy(f"Fixing Formula for {old} -> {new}...")
        problem_formula = [f for f in FormulaService.get_all() if old in f.equation]
        for pf in problem_formula:
            new_eqn = str(pf.equation).replace(old, new)
            FormulaService.get(id=pf.id).equation = new_eqn
            FormulaService.commit()

def fix_unit():
    # DO UNIT FIX
    for par, new_unit in UNIT_FIXES.items():
        loggy(f"Fixing units for {par} -> {new_unit}...")
        par_def = ParameterService.definitions.get(variable_name=par)
        if par_def:
            def_unit = par_def.default_unit
            if not def_unit == new_unit:
                par_def.default_unit = new_unit
            for cp in ParameterService.get_all(definition_id=par_def.id):
                if not cp.unit == new_unit:
                    cp.unit = new_unit
            ParameterService.commit()


def fix_formula():
    formulas = [f for f in FormulaService.get_all() if f.equation == "(((10 ** (- 1.5 + 0.4 * math.log10(self.K_ow))) if (math.log10(self.K_ow) < 3 else ((0.5) if (math.log10(self.K_ow) >= 3) and (math.log10(self.K_ow) < 6) else (10 ** (1.2 - 0.25 * math.log10(self.K_ow)))))) if compartment.BW > 0.1 else ((10 ** (- 2.6 + 0.5 * math.log10(self.K_ow))) if (math.log10(self.K_ow) < 5 else ((0.8) if (math.log10(self.K_ow) >= 5) and (math.log10(self.K_ow) < 6) else (10 ** (2.9 - 0.5 * math.log10(self.K_ow))))))) if compartment.media.id in {33 , 32 , 29 , 27 , 28} else 0"]
    if len(formulas) > 0:
        for formula in formulas:
            FormulaService.get(formula.id).equation = '(((10 ** (- 1.5 + 0.4 * math.log10(self.K_ow)) if math.log10(self.K_ow) < 3 else (0.5 if (math.log10(self.K_ow) >= 3 and math.log10(self.K_ow) < 6) else 10 ** (1.2 - 0.25 * math.log10(self.K_ow)))) if compartment.BW.magnitude > 0.1 else (10 ** (- 2.6 + 0.5 * math.log10(self.K_ow)) if math.log10(self.K_ow) < 5 else (0.8 if (math.log10(self.K_ow) >= 5 and math.log10(self.K_ow) < 6) else 10 ** (2.9 - 0.5 * math.log10(self.K_ow))))) if compartment.media.id in {32 , 33 , 27 , 28 , 29} else 0)'

    # f = [f for f in FormulaService.get_all() if
    #      f.equation == '0.3262149134948966 * chemical.ParticleVolumetricDRYDepositionRate(receiver) * sender.linked_compartments(media="$Leaf" , same_parcel=True)[0].DryDepInterceptionFraction * sender.interface_with(receiver) / sender.Volume']
    # if len(f) > 0:
    #     f = f[0]
    #     FormulaService.get(f.id).equation = 'sender.AllowExchange_forOther * chemical.ParticleVolumetricDRYDepositionRate(receiver) * sender.linked_compartments(media="$Leaf" , same_parcel=True)[0].DryDepInterceptionFraction * sender.interface_with(receiver) / sender.Volume'

    # f = [f for f in FormulaService.get_all() if
    #      f.equation == '0.02359582829896095 * chemical.ParticleVolumetricWetDepositionRate(sender) * sender.linked_compartments(media="$Leaf" , same_parcel=True)[0].WetDepInterceptionFraction * receiver.volume_element.parcel.area / sender.Volume if (environment.Rain > 0 and sender.Volume > 0) else 0']
    # if len(f) > 0:
    #     f = f[0]
    #     FormulaService.get(f.id).equation = 'sender.AllowExchange_forOther * chemical.ParticleVolumetricWetDepositionRate(sender) * sender.linked_compartments(media="$Leaf" , same_parcel=True)[0].WetDepInterceptionFraction * receiver.volume_element.parcel.area / sender.Volume if (environment.Rain > 0 and sender.Volume > 0) else 0'

    # f = [f for f in FormulaService.get_all() if
    #      f.equation == '((sender.SedimentDepositionRate / sender.rho)) * (chemical.FractionMass_Sorbed(sender) / sender.VolumeFraction_Solid) * (sender.interface_with(receiver)) / sender.Volume']
    # if len(f) > 0:
    #     f = f[0]
    #     FormulaService.get(f.id).equation = '((sender.SedimentDepositionRate / receiver.rho)) * (chemical.FractionMass_Sorbed(sender) / sender.VolumeFraction_Solid) * (sender.interface_with(receiver)) / sender.Volume'
    #
    # f = [f for f in FormulaService.get_all() if
    #      f.equation == '((sender.SedimentDepositionRate / receiver.rho)) * (chemical.FractionMass_Sorbed(sender) / sender.VolumeFraction_Solid) * (sender.interface_with(receiver)) / sender.Volume']
    # if len(f) > 0:
    #     f = f[0]
    #     FormulaService.get(f.id).equation = '((sender.SedimentDepositionRate / receiver.rho)) * (chemical.FractionMass_Sorbed(sender) / (sender.SuspendedSedimentConcentration / receiver.rho)) * (sender.interface_with(receiver)) / sender.Volume'

    FormulaService.commit()


def add_ps_algs():
    for p in PS_ALG_PARS:
        if p.get("formula"):
            for d in p['domain_ids']:
                new_formula = FormulaService.get_or_create(equation=p['formula'])
                # Fix self as chemical for the new formula Arguments where applies
                self_arr = [fa for fa in new_formula._arguments if fa.name == "self"]
                if len(self_arr) > 0:
                    self_arr[0].domain_id = d
                if p['unit']:
                    ParameterService.definitions.get_or_create(variable_name=p['name'], full_name=p['name'],
                                                               domain_id=d,
                                                               default_unit=p['unit'],
                                                               default_formula_id=new_formula.id)
                else:
                    ParameterService.definitions.get_or_create(variable_name=p['name'], full_name=p['name'],
                                                               domain_id=d,
                                                               default_formula_id=new_formula.id)
                loggy(f'Added new formula parameter {p["name"]} for domain {d}')
                ParameterService.commit()
            FormulaService.commit()
        elif 'value' in p:
            for d in p['domain_ids']:
                if p['unit']:
                    ParameterService.definitions.get_or_create(variable_name=p['name'], full_name=p['name'],
                                                               domain_id=d,
                                                               default_unit=p['unit'], default_value=p.get("value"))
                else:
                    ParameterService.definitions.get_or_create(variable_name=p['name'], full_name=p['name'],
                                                               domain_id=d,
                                                               default_value=p.get("value"))
                loggy(f'Added new value parameter {p["name"]} for domain {d}')
                ParameterService.commit()
        else:
            continue
    # Now add the algorithm
    for alg in PS_ALGS:
        try:
            new_formula = FormulaService.get_or_create(equation=alg['eqn'])
            TransportProcessService.get_or_create(name=alg['name'], algorithm_id=new_formula.id, category=alg['type'],
                                                requirements=alg['reqs'])
            loggy(f'Added new Transport Algorithm parameter {alg["name"]}')
            TransportProcessService.commit()
            FormulaService.commit()
        except IntegrityError as e:
            loggy(f'Duplicate Transport Algorithm entry found: {alg["name"]}')


def update_ps_algs():
    for alg in ALG_UPDATES:
        alg_obj = TransportProcessService.get(name=alg['name'], category=alg['type'], requirements=alg['reqs'])
        frm_obj = alg_obj.algorithm
        if frm_obj.equation == alg['eqn']:
            loggy(f'Formula already up-to-date for {alg["name"]}')
            continue
        else:
            FormulaService.get(frm_obj.id).equation = alg['eqn']
            loggy(f'Updated Transport Algorithm equation for {alg["name"]}')
            FormulaService.commit()


def fix_requirements_for_ps_algs_organics():
    for psa in PS_ALGS:
        try:
            tp = TransportProcessService.get(name=psa["name"])
            if '(chemical.isa("Organic"))' in tp.requirements:
                loggy(f"REQUIREMENT ALREADY EXISTS FOR {tp.name}. Skipping...")
                continue
            else:
                tp.requirements = tp.requirements.replace("(chemical.id == 24)", '(chemical.isa("Organic"))')
                loggy(f"FIXED REQUIREMENT FOR {tp.name}. Continuing...")
                TransportProcessService.commit()
        except IntegrityError as e:
            loggy(f'Duplicate Transport Algorithm entry found: {psa["name"]}')


def update_parameter_def():
    for pd in UPDATE_PARS:
        if pd["default_value"]:
            par = ParameterService.definitions.get(variable_name=pd["variable_name"], domain_id=pd["domain_id"])
            par.default_value = pd["default_value"]


def add_new_parameter_defs():
    for pd in NEW_PARAMETER_DEFS:
        if pd["default_formula"]:
            # Check if formula already exists specific to that domain
            ff = [f for f in FormulaService.get_all() if f.equation == pd["default_formula"] and f.arguments.get("self")]
            nf = [f for f in ff if f.arguments.get("self").domain_id == pd["domain_id"]]
            if len(nf) == 0:
                # No existing formula so create
                nf = FormulaService.create(equation=pd["default_formula"])
                self_arr = [fa for fa in nf._arguments if fa.name == "self" and not fa.domain_id]
                if len(self_arr) > 0:
                    self_arr[0].domain_id = pd["domain_id"]
                ParameterService.definitions.get_or_create(variable_name=pd["variable_name"], full_name=pd["full_name"],
                                                           domain_id=pd["domain_id"], default_unit=pd["default_unit"],
                                                           default_formula_id=nf.id)
                loggy(f"CREATED NEW FORMULA AND PARAMETER {pd['variable_name']} FOR DOMAIN ID {pd['domain_id']}")
            else:
                loggy(f"THERE IS ALREADY AN EXISTING FORMULA FOR {pd['variable_name']} FOR DOMAIN ID {pd['domain_id']}")
                nf = nf[0]
                loggy(f"CREATING/GETTING PARAMETER DEFINITION FOR {pd['variable_name']} FOR DOMAIN ID {pd['domain_id']}")
                ParameterService.definitions.get_or_create(variable_name=pd["variable_name"], full_name=pd["full_name"],
                                                           domain_id=pd["domain_id"], default_unit=pd["default_unit"],
                                                           default_formula_id=nf.id)
        else:
            ParameterService.definitions.get_or_create(variable_name=pd["variable_name"], full_name=pd["full_name"],
                                                       domain_id=pd["domain_id"], default_unit=pd["default_unit"],
                                                      default_value=pd["default_value"])
        FormulaService.commit()
        ParameterService.commit()


def fix_chem_formula_arguments():
    ff = [f for f in FormulaService.get_all() if f.arguments.get("chemical")]
    nf = [f for f in ff if not f.arguments.get("chemical").domain_id]
    for f in nf:
        chem_arr = [fa for fa in f._arguments if fa.name == "chemical" and not fa.domain_id]
        if len(chem_arr) > 0:
            chem_arr[0].domain_id = 2


def fix_surface_water_vol_element_bounds():
    for scn in SCENARIO_NAMES:
        s = ScenarioService.get(name=scn)
        for p in s.parcels:
            sw_comps = [c for c in p.compartments if c.media.isa("Surface_Water")]
            if len(sw_comps) > 0:
                csw = sw_comps[0]
                h_diff = (csw.height - csw.MeanDepth).magnitude
                if h_diff == 0:
                    loggy(f"Scenario {scn}: The depth for Volume element {csw.volume_element.standard_name} already fixed. SKIPPING...")
                    continue
                # Now shift bounds of everything below the SW volume element
                ves = [a for a in p.volume_elements]
                for ve in ves:
                    if ve.top <= csw.volume_element.bottom:
                        print(f'scenario {s.name}: New {ve.name} top = {ve.top + h_diff} and bottom = {ve.bottom + h_diff}')
                        ve.top = ve.top + h_diff
                        ve.bottom = ve.bottom + h_diff
                # finally fix the surface water element bottom
                csw.volume_element.bottom = -1 * csw.MeanDepth.magnitude
        VolumeElementService.commit()


def fix_domain_specific_param_formula():
    for dp in DOMAIN_SPECIFIC_PARAM_FORMULA_REPLACEMENTS:
        domain = ParameterService.domains.get(name=dp['domain'])
        if not domain:
            loggy(f'THE DOMAIN NAME: {dp["domain"]} DOES NOT EXIST!!!')
            continue
        domain_id = domain.id
        pd = ParameterService.definitions.get(variable_name=dp['variable_name'], domain_id=domain_id)
        dom_formula = pd.default_formula
        frm = FormulaService.get(dom_formula.id)
        frm.equation = frm.equation.replace(dp['old_formula'], dp['new_formula'])
        FormulaService.commit()


def delete_comp_specific_custom_param():
    for scn in SCENARIO_NAMES:
        s = ScenarioService.get(name=scn)
        for par in CUSTOM_PARS_TO_DELETE:
            par_name = par["par_name"]
            comp_media = par["comp_media"]
            for c in s.compartments:
                if c.media.isa(comp_media):
                    p = c.parameters.get(par_name)
                    if isinstance(p, CustomParameter):
                        print(f'Deleting Custom parameter, {par_name}, for {c.standard_name} in scenario {s.name}')
                        ParameterService.delete(p.id)
                    else:
                        print(f'No Custom parameter, {par_name}, found for {c.standard_name}. Skipping...')
            ParameterService.commit()


def transfer_custom_param_domain_to_chem(ch_list):
    if not ch_list:
        chems = [
            "Benzo(A)Pyrene",
            "Divalent Mercury",
            "Elemental Mercury",
            "MethylMercury",
            "2,3,7,8-TCDD",
            "Cadmium",
            "Arsenic"
        ]
    else:
        chems = ch_list

    new_dom = ParameterService.domains.get(name="Chemical")
    for chem in chems:
        ch = ChemicalService.get(name=chem)
        if not ch:
            loggy(f'No chemical with name {chem}')
            continue
        cpars = [p for p in ParameterService.get_all(scenario_id=1) if
                 p.domain.name != "Chemical" and p.requirements == f"(self.id == {ch.id})" and isinstance(p, CustomParameter)]
        if len(cpars) == 0:
            loggy(f'custom parameter domains for chemical, {chem}, has already been fixed!!!')
            continue
        for cpar in cpars:
            old_par_def = cpar.definition
            new_par_def = ParameterService.definitions.get(variable_name=old_par_def.variable_name, domain_id=new_dom.id)
            if new_par_def:
                if old_par_def == new_par_def:
                    loggy(f'{old_par_def.variable_name} already had the domain fixed!!!')
                    continue
                loggy(f'{old_par_def.variable_name} form domain {cpar.domain.name} to {new_dom.name}')
                cpar.definition = new_par_def
                ParameterService.commit()
            else:
                loggy(
                    f"UH-OH!! Parameter Definition for {old_par_def.variable_name} with domain {new_dom.name} does not exist!! Creating...")
                new_par_def = ParameterService.definitions.create(variable_name=old_par_def.variable_name,
                                                                  full_name=old_par_def.variable_name, domain_id=new_dom.id,
                                                                  default_unit=old_par_def.default_unit)
                loggy(
                    f'{old_par_def.variable_name} form domain {cpar.domain.name} to new definition with domain: {new_dom.name}')
                cpar.definition = new_par_def
                ParameterService.commit()


def add_more_chemicals():
    for ch in CHEMS_TO_ADD:
        loggy(f'{80 * "#"}')
        loggy(f'{40 * "#"} Checking new chemical {ch}')
        run_chem_migrations(ch, mode="check")
        loggy(f'{40 * "#"} Checking {ch} complete')
        loggy(f'{40 * "#"} Adding chemical parameters for {ch}')
        run_chem_migrations(ch, mode="chem")
        loggy(f'{40 * "#"} Adding chemical parameters for {ch} complete')
        loggy(f'{40 * "#"} Adding compartment parameters for {ch}')
        run_chem_migrations(ch, mode="comp")
        loggy(f'{40 * "#"} Adding compartment parameters for {ch} complete')
        loggy(f'{20 * "#"} Done importing {ch} {20 * "#"}')


def loggy(s):
    msg = f"[Patcher] {dt.now()}: {s}"
    print(msg)


if __name__ == '__main__':
    '''THIS PATCH IS DESIGNED TO BE APPLIED TO MIGRATION WITH FILENAME aws_pytrim_05-09-2025.sql 
    IT CAN HANDLE EXISTING PARAMETERS AND IGNORE THEM BUT IT IS NOT FULLY TESTED FOR LATER MIGRATIONS.
    IF YOU ARE UNSURE, YOU CAN COMMENT OUT THE CALLS AT THE BOTTOM IF YOU THINK  THEY CAN OVERWRITE YOUR DATA OR REVERT 
    YOUR CHANGES'''
    # from trim_db.utils.users_roles import implement_users_roles
    #
    # try:
    #     import time
    #     implement_users_roles()
    #     time.sleep(5)
    # except Exception as e:
    #     print(f'-- Unable to create Users/Roles.\n{e}')

    try:
        ScenarioService.get(id=2)
    except Exception as e:
        print(e)
        raise

    # fix_custom_links()
    # do_formula_replacements()
    # run_chem_migrations("Benzo(A)Pyrene", mode="chem")
    # run_chem_migrations("Benzo(A)Pyrene", mode="comp")
    # run_chem_migrations("Elemental Mercury", mode="comp")
    # run_chem_migrations("Divalent Mercury", mode="comp")
    # run_chem_migrations("MethylMercury", mode="comp")
    # run_chem_migrations("2,3,7,8-TCDD", mode="chem")
    # run_chem_migrations("2,3,7,8-TCDD", mode="comp")
    # run_chem_migrations("Cadmium", mode="check")
    # run_chem_migrations("Cadmium", mode="chem")
    # run_chem_migrations("Cadmium", mode="comp")
    # run_chem_migrations("Arsenic", mode="check")
    # run_chem_migrations("Arsenic", mode="chem")
    # run_chem_migrations("Arsenic", mode="comp")
    # do_formula_replacements()
    # fix_formula()
    # fix_unit()
    # add_ps_algs()
    # update_ps_algs()
    # fix_chem_formula_arguments()
    # fix_requirements_for_ps_algs_organics()
    # add_new_parameter_defs()
    # update_parameter_def()
    # fix_surface_water_vol_element_bounds()
    # fix_domain_specific_param_formula()
    # delete_comp_specific_custom_param()
    # transfer_custom_param_domain_to_chem()

    # NEW TERM FOR PYTRIM ----->
    add_more_chemicals()
    do_formula_replacements()
    fix_formula()
    fix_unit()
    transfer_custom_param_domain_to_chem(CHEMS_TO_ADD)
