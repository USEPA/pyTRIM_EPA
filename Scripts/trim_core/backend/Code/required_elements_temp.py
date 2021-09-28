## for two compartment test case

required_compartments = ["advection sink",\
            "degradation/reaction sink",\
            "flush rate sink",\
            "sediment",\
            "sediment burial sink",\
            "surface water",\
            "air",\
            "macrophyte",\
            'zooplankton',\
            'benthic invertebrate',\
            "benthic omnivore",\
            'benthic carnivore',\
            "water column carnivore",\
            "water column herbivore",\
            "water column omnivore",\
            ]

required_algorithms = [\
            "degradation/reaction sink in sediment(alginstid_4565)",\
            "degradation/reaction sink in surface water(alginstid_4585)",\
            "demethylation(mhg -> hg2) in abiotic media, rate is input(alginstid_1892)",\
            "diffusion from sediment to surface water, fugacity-based(alginstid_2195)",\
            "diffusion from surface water to sediment, fugacity-based(alginstid_2149)",\
            "methylation(hg2 -> mhg) in abiotic media, rate is input(alginstid_1891)",\
            "oxidation(hg0 -> hg2) in abiotic media, rate is input(alginstid_1894)",\
            "reduction(hg2 -> hg0) in abiotic media, rate is input(alginstid_1893)",\
            "resuspension from sediment to surface water, general(alginstid_2190)",\
            "sediment burial from sediment to sediment burial sink, zero net deposition, general(alginstid_4135)",\
            "sediment deposition from surface water to sediment, general(alginstid_2139)",\


            "fish bioenergetic model - ingestion of algae by fish(alginstid_1527)",\
            "fish bioenergetic model - ingestion of algae by zooplankton",\
            "fish bioenergetic model - ingestion of benthic carnivore by benthic omnivore(alginstid_1455)",\
            "fish bioenergetic model - ingestion of benthic carnivore by water column carnivore(alginstid_2245)",\
            "fish bioenergetic model - ingestion of benthic carnivore by water column omnivore(alginstid_2277)",\
            "fish bioenergetic model - ingestion of benthic invertebrate by benthic carnivore(icfid_08-001)",\
            "fish bioenergetic model - ingestion of benthic invertebrate by benthic omnivore(alginstid_1467)",\
            "fish bioenergetic model - ingestion of benthic invertebrate by water column carnivore(alginstid_2255)",\
            "fish bioenergetic model - ingestion of benthic invertebrate by water column herbivore(alginstid_2270)",\
            "fish bioenergetic model - ingestion of benthic invertebrate by water column omnivore(alginstid_2287)",\
            "fish bioenergetic model - ingestion of benthic omnivore by benthic carnivore(alginstid_1447)",\
            "fish bioenergetic model - ingestion of benthic omnivore by water column carnivore(alginstid_2250)",\
            "fish bioenergetic model - ingestion of benthic omnivore by water column omnivore(alginstid_2282)",\
            "fish bioenergetic model - ingestion of macrophyte by water column herbivore(alginstid_1646)",\
            "fish bioenergetic model - ingestion of macrophyte by water column omnivore(alginstid_1655)",\
            "fish bioenergetic model - ingestion of water column carnivore by benthic carnivore(alginstid_2158)",\
            "fish bioenergetic model - ingestion of water column carnivore by benthic omnivore(alginstid_2175)",\
            "fish bioenergetic model - ingestion of water column carnivore by water column omnivore(alginstid_1618)",\
            "fish bioenergetic model - ingestion of water column herbivore by benthic carnivore(alginstid_2163)",\
            "fish bioenergetic model - ingestion of water column herbivore by benthic omnivore(alginstid_2180)",\
            "fish bioenergetic model - ingestion of water column herbivore by water column carnivore(alginstid_1600)",\
            "fish bioenergetic model - ingestion of water column herbivore by water column omnivore(alginstid_1638)",\
            "fish bioenergetic model - ingestion of water column omnivore by benthic carnivore(alginstid_2168)",\
            "fish bioenergetic model - ingestion of water column omnivore by benthic omnivore(alginstid_2185)",\
            "fish bioenergetic model - ingestion of water column omnivore by water column carnivore(alginstid_1610)",\
            "fish bioenergetic model - ingestion of zooplankton by water column herbivore",\
            
            'exchange from macrophyte to surface water(alginstid_1547)',\
            'degradation/reaction sink in macrophyte',\
            'oxidation(hg0 -> hg2) in macrophytes',\
            'time-dependent partition from surface water to macrophyte, hg(alginstid_1549)',\
            'time-dependent partition from macrophyte to surface water(alginstid_1544),hg',\

            'time-dependent partition from sediment to benthic invertebrate(alginstid_1438)',\
            'time-dependent partition from benthic invertebrate to sediment(alginstid_1433)',\

            
            'degradation/reaction sink in zooplankton(alginstid_4570_z)',\
            'elimination from zooplankton to surface water',\
            'elimination from fish to surface water(alginstid_1512)',\

            "demethylation (mhg->hg2) in fish(alginstid_1446)",\
            'oxidation(hg0 -> hg2) in fish(alginstid_1443)',\
            'reduction(hg2 -> hg0) in fish(alginstid_1444)',\

            "bulk advection from surface water to flush-rate advection sink, general(alginstid_4125)",\
    	    "diffusion from surface water to air, two film(alginstid_4080)-hg",\
            "algae deposition from surface water to sediment, general(alginstid_2144)",\
           
]