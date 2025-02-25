## adding surface soil test case
## for two compartment test case

# required compartments refer to primary abiotic types 

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
            "soil - surface",\
            "leaf - deciduous forest in deciduous forest",\
            "leaf - coniferous forest in coniferous forest",\
            "leaf particle - deciduous forest in deciduous forest",\
            "leaf particle - coniferous forest in coniferous forest",\

            "leaf - deciduous forest",\
            "leaf particle - deciduous forest",\
                
            "soil - root zone",\
            "soil - vadose zone",\
            "groundwater",\
            "leaf - grasses/herbs in grasses/herbs",\
            "leaf particle - grasses/herbs in grasses/herbs",\
            "root - grasses/herbs in grasses/herbs",\
            "stem - grasses/herbs in grasses/herbs",\
                ]

required_algorithms = [\
            "demethylation(mhg -> hg2) in abiotic media, rate is input(alginstid_1892)",\
            "diffusion from sediment to surface water, fugacity-based(alginstid_2195)",\
            "diffusion from surface water to sediment, fugacity-based(alginstid_2149)",\
            "methylation(hg2 -> mhg) in abiotic media, rate is input(alginstid_1891)",\
            "oxidation(hg0 -> hg2) in abiotic media, rate is input(alginstid_1894)",\
            "reduction(hg2 -> hg0) in abiotic media, rate is input(alginstid_1893)",\
            "resuspension from sediment to surface water, general(alginstid_2190)",\
            "sediment burial from sediment to sediment burial sink, zero net deposition, general(alginstid_4135)",\
            "sediment deposition from surface water to sediment, general(alginstid_2139)",\

            "degradation/reaction sink in air(alginstid_4675)",\
            "degradation/reaction sink in benthic invertebrate(alginstid_4580)",\
            "degradation/reaction sink in fish(alginstid_4570)",\
            "degradation/reaction sink in groundwater(alginstid_4145)",\
            "degradation/reaction sink in leaf(alginstid_4165)",\
            "degradation/reaction sink in macrophyte",\
            "degradation/reaction sink in root zone(alginstid_4155)",\
            "degradation/reaction sink in root(alginstid_4175)",\
            "degradation/reaction sink in sediment(alginstid_4565)",\
            "degradation/reaction sink in stem(alginstid_4170)",\
            "degradation/reaction sink in surface soil(alginstid_4160)",\
            "degradation/reaction sink in surface water(alginstid_4585)",\
            "degradation/reaction sink in vadose zone(alginstid_4150)",\
            "degradation/reaction sink in zooplankton(alginstid_4570_z)",\

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
            
            "exchange from surface water to macrophyte(alginstid_1552)",\
            'exchange from macrophyte to surface water(alginstid_1547)',\
            'degradation/reaction sink in macrophyte',\
            'oxidation(hg0 -> hg2) in macrophytes',\
            "time-dependent partition from surface water to macrophyte, cd(alginstid_1549)",\
            'time-dependent partition from surface water to macrophyte, hg(alginstid_1549)',\
            'time-dependent partition from macrophyte to surface water(alginstid_1544),hg',\
            "time-dependent partition from macrophyte to surface water(alginstid_1544),cd",\


            "exchange from surface water to zooplankton, organics(alginstid_1517_z)",\
            "exchange from surface water to zooplankton, cd (alginstid_cdabs_z)",\
            "exchange from surface water to zooplankton, pb",\

            "exchange from fish to surface water, organics(alginstid_1515)",\

            'time-dependent partition from sediment to benthic invertebrate(alginstid_1438)',\
            'time-dependent partition from benthic invertebrate to sediment(alginstid_1433)',\
            "exchange from sediment to benthic invertebrate, interacts with pore water, pahs",\
            "exchange from benthic invertebrate to sediment, pahs",\
            
            'degradation/reaction sink in zooplankton(alginstid_4570_z)',\
            'elimination from zooplankton to surface water',\
            'elimination from fish to surface water(alginstid_1512)',\

            "exchange from surface water to fish, cd",\
            "exchange from surface water to fish, pb",\
            "exchange from surface water to fish, organics(alginstid_1517)",\
            "demethylation (mhg->hg2) in fish(alginstid_1446)",\
            'oxidation(hg0 -> hg2) in fish(alginstid_1443)',\
            'reduction(hg2 -> hg0) in fish(alginstid_1444)',\

            "bulk advection from surface water to flush-rate advection sink, general(alginstid_4125)",\
    	    "diffusion from surface water to air, two film(alginstid_4080)-hg",\
            "algae deposition from surface water to sediment, general(alginstid_2144)",\

            'waterflow from surface water to surface water, general(alginstid_3685)',\
                
            'runoff from surface soil to soil advection sink',\
            'erosion from surface soil to surface soil, general(alginstid_2460)',\
            'runoff from surface soil to surface soil, general(alginstid_2465)',\
            'erosion from surface soil to surface water, general(alginstid_3515)',\
            'runoff from surface soil to surface water, general(alginstid_3520)',\
            'erosion from surface soil to soil advection sink',\

            "diffusion from surface soil to air, hg0(alginstid_3997)",\
            "diffusion from surface soil to air, mhg(alginstid_3999)",\
            "diffusion from surface soil to air, organics(alginstid_3995)",\

            "resuspension from surface soil to air, set to deposition rate of particles(alginstid_4000)",\
                
            "litterfall from leaves to soil(alginstid_1088)",\
            "litterfall of leaf particle to soil(alginstid_1098)",\
                
            "diffusion from plant leaf to air, hg0, default (bennett 1998)(alginstid_4005)",\
            "diffusion from plant leaf to air, mhg, default (bennett 1998)(alginstid_4005)",\
            "diffusion from plant leaf to air, organics, default (bennett 1998)(alginstid_4005)",\
            "demethylation(mhg -> hg2) in plant leaves, rate is input(alginstid_1249)",\
            "demethylation(mhg -> hg2) in plant stem, rate is input(alginstid_1271)",\
            "methylation(hg2 -> mhg) in plant leaves, rate is input(alginstid_1248)",\
            "methylation(hg2 -> mhg) in plant stem, rate is input(alginstid_1270)",\
            "particles blown off from plant leaf to air (dry)(alginstid_4010)",\
            "particles washed off leaf onto ground(alginstid_1103)",\
            "transfer from leaf particle on surface to leaf, cd(alginstid_1250)",\
            "transfer from leaf particle on surface to leaf, hg(alginstid_1250)",\
            "transfer from leaf particle on surface to leaf, organic(alginstid_1250)",\
            "transfer from leaf to leaf particle on surface, cd(alginstid_1255)",\
            "transfer from leaf to leaf particle on surface, hg(alginstid_1255)",\
            "transfer from leaf to leaf particle on surface, organic(alginstid_1255)",\
            "transfer from leaf to stem - agriculture, cd(alginstid_1265)",\
            "transfer from leaf to stem - agriculture, hg(alginstid_1265)",\
            "transfer from leaf to stem - agriculture, organic(alginstid_1265)",\
            "transfer from leaf to stem - grasses/herbs, cd",\
            "transfer from leaf to stem - grasses/herbs, hg",\
            "transfer from leaf to stem - grasses/herbs, organic",\
            "transfer from root zone to stem - agriculture, cd",\
            "transfer from root zone to stem - agriculture, hg",\
            "transfer from root zone to stem - agriculture, organic",\
            "transfer from root zone to stem - grasses/herbs, cd(alginstid_1944)",\
            "transfer from root zone to stem - grasses/herbs, hg(alginstid_1944)",\
            "transfer from root zone to stem - grasses/herbs, organics(alginstid_1944)",\
            "transfer from stem to leaf - agriculture, cd",\
            "transfer from stem to leaf - agriculture, hg",\
            "transfer from stem to leaf - agriculture, organic",\
            "transfer from stem to leaf - grasses/herbs, cd(alginstid_1260)",\
            "transfer from stem to leaf - grasses/herbs, hg(alginstid_1260)",\
            "transfer from stem to leaf - grasses/herbs, organic(alginstid_1260)",\

            "time-dependent partition from root zone to root, interacts with bulk soil - agriculture, cd(alginstid_1953)",\
            "time-dependent partition from root zone to root, interacts with bulk soil - agriculture, hg(alginstid_1953)",\
            "time-dependent partition from root zone to root, interacts with bulk soil - grasses/herbs,cd(alginstid_1952)",\
            "time-dependent partition from root zone to root, interacts with bulk soil - grasses/herbs,hg(alginstid_1952)",\
            "time-dependent partition from root zone to root, interacts with soil pore water - agriculture, organics",\
            "time-dependent partition from root zone to root, interacts with soil pore water - grasses/herbs, organics(alginstid_1949)",\
            "time-dependent partition from root to root zone, interacts with bulk soil - agriculture, cd(alginstid_1932)",\
            "time-dependent partition from root to root zone, interacts with bulk soil - agriculture, hg(alginstid_1932)",\
            "time-dependent partition from root to root zone, interacts with bulk soil - grasses/herbs, cd(alginstid_1933)",\
            "time-dependent partition from root to root zone, interacts with bulk soil - grasses/herbs, hg(alginstid_1933)",\
            "time-dependent partition from root to root zone, interacts with soil pore water - agriculture, organics",\
            "time-dependent partition from root to root zone, interacts with soil pore water - grasses/herbs, organics(alginstid_1929)",\
            "time-dependent partition from benthic invertebrate to bulk sediment for dioxins(icfid_08-003)",\
            "time-dependent partition from bulk sediment to benthic invertebrate for dioxins(icfid_08-002)",\

                
            "diffusion from root zone to surface soil(alginstid_1939)",\
            "diffusion from surface soil to root zone(alginstid_1919)",\
            "percolation from surface soil to root zone(alginstid_1924)",\
            "degradation/reaction sink in root zone(alginstid_4155)",\
                
            "diffusion from vadose zone to root zone(alginstid_1914)",\
            "degradation/reaction sink in vadose zone(alginstid_4150)",\
            "diffusion from root zone to vadose zone(alginstid_1904)",\
            "percolation from root zone to vadose zone(alginstid_1909)",\
          # "diffusion from vadose zone to vadose zone(alginstid_2445)",\ #turning this off because we dont accommodate above or below relationshipts
            "diffusion from vadose zone to root zone(alginstid_1914)",\
                
            "percolation from vadose zone to groundwater(alginstid_1899)",\
            "recharge from groundwater to surface water, general(alginstid_3510)",\
            "degradation/reaction sink in groundwater(alginstid_4145)",\
  
            "exchange from benthic invertebrate to sediment, pahs",\
            "exchange from benthic invertebrate to sediment, dioxins",\
            "exchange from sediment to benthic invertebrate, interacts with pore water, pahs",\
            "exchange from sediment to benthic invertebrate, interacts with pore water, dioxins",\
            "diffusion from surface water to air, two film(alginstid_4080)-organic",\

             'wet deposition of vapor phase from air to surface water, hg2(alginstid_3708)',\
             'diffusion from air to plant leaf, hg0, default(riederer 1995)',\
             'diffusion from air to surface water, organics, two film(alginstid_3710)',\
             'advection from air to air(alginstid_4075)',\
             'dry deposition of vapor from air to surface soil(alginstid_2488)',\
             'wet deposition of particles from air to surface water(alginstid_3700)',\
             'diffusion from air to surface soil, organics(alginstid_2505)',\
             'wet deposition of vapor phase from air to surface soil, hg0',\
             'diffusion from air to surface water, hg0, two film(alginstid_3710)',\
             'diffusion from air to plant leaf, organics, default(riederer 1995)',\
             'diffusion from air to surface water, mhg, two film(alginstid_3710)',\
             'diffusion from air to plant leaf, mhg, default(riederer 1995)',\
             'advection from air to air, steady-state approx',\
             'bulk advection from air to advection sink, general(alginstid_4095)',\
             'diffusion from air to plant leaf, organics, alternative (bennett 1998)(alginstid_2515)',\
             'wet deposition of vapor phase from air to surface water, organics(alginstid_3705)',\
             'wet deposition of particles from air to plants',\
             'dry deposition of particles from air to soil(alginstid_2490)',\
             'bulk advection from air to advection sink, steady-state approx',\
             'diffusion from air to plant leaf, mhg, alternative (bennett 1998)(alginstid_2515)',\
             'diffusion from air to surface soil, hg0(alginstid_2507)',\
             'dry deposition of particles from air to plants',\
             'dry deposition of vapor from air to surface water(alginstid_3693)',\
             'dry deposition of particles from air to surface water(alginstid_3695)',\
             'dry deposition of vapor from air to plants',\
             'diffusion from air to plant leaf, hg0, alternative (bennett 1998)(alginstid_2515)',\
             'wet deposition of vapor phase from air to surface soil, hg2',\
             'wet deposition of vapor phase from air to surface soil, organics',\
             'diffusion from air to surface soil, mhg(alginstid_2509)',\
             'wet deposition of vapor phase from air to surface water, hg0(alginstid_3707)',\
             'wet deposition of particles to surface soil(alginstid_2495)',\
             'wet deposition of vapor phase to plant leaf from air, hg0(alginstid_2512)',\
             'wet deposition of vapor phase to plant leaf from air, hg2',\
             'wet deposition of vapor phase to plant leaf from air, organics(alginstid_2510)',\
                 ]                
