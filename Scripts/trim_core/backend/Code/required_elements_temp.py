## for two compartment test case

required_compartments = ["Advection Sink",\
            "Degradation/Reaction Sink",\
            "Flush Rate Sink",\
            "Sediment",\
            "Sediment Burial Sink",\
            "Surface water",\
            ]

required_algorithms = [\
            "Degradation/Reaction Sink in Sediment(AlgInstID_4565)",\
            "Degradation/Reaction Sink in Surface Water(AlgInstID_4585)",\
            "Demethylation(MHg -> Hg2) in Abiotic Media, Rate is input(AlgInstID_1892)",\
            "Diffusion from Sediment to Surface Water, Fugacity-based(AlgInstID_2195)",\
            "Diffusion from Surface Water to Sediment, Fugacity-based(AlgInstID_2149)",\
            "Methylation(Hg2 -> MHg) in Abiotic Media, Rate is input(AlgInstID_1891)",\
            "Oxidation(Hg0 -> Hg2) in Abiotic Media, Rate is input(AlgInstID_1894)",\
            "Reduction(Hg2 -> Hg0) in Abiotic Media, Rate is input(AlgInstID_1893)",\
            "Resuspension from Sediment to Surface Water, General(AlgInstID_2190)",\
            "Sediment Burial from Sediment to Sediment Burial Sink, Zero net deposition, General(AlgInstID_4135)",\
            "Sediment Deposition from Surface Water to Sediment, General(AlgInstID_2139)",\
	    "Bulk Advection from Surface Water to Flush-rate Advection Sink, General(AlgInstID_4125)",\
]