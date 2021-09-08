## for two compartment test case

required_compartments = ["advection sink",\
            "degradation/reaction sink",\
            "flush rate sink",\
            "sediment",\
            "sediment burial sink",\
            "surface water",\
            "air",\
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
	    "bulk advection from surface water to flush-rate advection sink, general(alginstid_4125)",\
	    "diffusion from surface water to air, two film(alginstid_4080)-hg",\
        "algae deposition from surface water to sediment, general(alginstid_2144)",
]