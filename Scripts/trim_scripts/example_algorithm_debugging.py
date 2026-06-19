from base import *

"""
Algorithm debugging, tracking down algorithm issues

Example access
    ENTITY.[param_name] gets the value of a parameter (possibly taking arguments)
        - receiver.TransferFactorToSoilNonConiferousLeaf(chem)`

    ENTITY.parameters.get(param_name) gets the actual parameter object (either a definition or a custom parameter)
        - receiver.parameters.get('TransferFactorToSoilNonConiferousLeaf').formula.id
"""

example_scenario_id = 138  # Tier1_Hg


def equation_check_1():
    """
    - looking at the core / algorithms file to track down the internal names
        - these are mapped in the transport_process table
        - can look up by name
    - getting the compartment names
    - breaking down the transport process equation
        - tp.algorithm.equation
    """
    s = ScenarioService.get(example_scenario_id)
    ve = s.get_volume_element(name="Sed_Pond")
    sender = ve.get_compartment(name="Sediment in Sed_Pond")
    receiver = ve.get_compartment(name="Burial_Sink in Sed_Pond")
    links = sender.get_links(receiver)

    for chem in s.chemicals:
        print(f"{s} :: {chem.name}")

        # for a given chemical, pull all transport processes (algorithms)
        tps = links[0].transport_processes(chemical=chem)
        tp = tps[0]
        # print(tp.algorithm.equation)

        print(f'solidarealphasevelocity = {sender.SedimentBurialRateToHaveZeroNetDeposition.to("m^3 / m^2 / day")}')
        print(f"sendingcompartment.chemical_fractionmass_sorbed = {chem.FractionMass_Sorbed(sender)}")
        print(f"sendingcompartment.volumefraction_solid = {sender.VolumeFraction_Solid}")
        print(
            f"Interfacial area between compartments = {sender.volume_element.interface_with(receiver.volume_element)}"
        )
        print(f"sendingcompartment.volume = {sender.Volume}")
        print("\n-----------------------------\n")
        # result = tp.evaluate(chemical=chem, sender=sender, receiver=receiver)


def equation_check_2():
    """
    More specific checks, sender/receiver
    """
    tp = TransportProcessService.get(algorithm_id=2608)
    eq = tp.algorithm.equation

    s = ScenarioService.get(example_scenario_id)
    chem = s.chemicals[1]  # id = 32
    ve = s.get_volume_element(name="SurfSoil")
    receiver = ve.get_compartment(media="Abiotic|Soil|Surface_Soil")[0]

    val = receiver.TransferFactorToSoilNonConiferousLeaf(chem)
    receiver.parameters.get("TransferFactorToSoilNonConiferousLeaf").formula.equation


def equation_check_3():
    """
    Diffusion from DryVaporSource to Surface Soil, Hg0
    """
    tp = TransportProcessService.get(algorithm_id=2608)  # Diffusion from DryVaporSource to Surface Soil, Hg0
    eq = tp.algorithm.equation

    s = ScenarioService.get(example_scenario_id)  # Tier1_Hg
    pcl = ParcelService.get(2737)  # N4
    chem = s.chemicals[1]  # id = 32, Elemental Hg

    sender = pcl.get_compartment(media="Source|Dry_Vapor")[0]
    receiver = pcl.get_compartment(media="Abiotic|Soil|Surface_Soil")[0]

    if receiver.return_sameparcel_linked_media_id_or_none(media="$Leaf") in {37, 41, 43}:
        receiver.TransferFactorToSoilNonConiferousLeaf(chem)
    elif receiver.return_sameparcel_linked_media_id_or_none(media="$Leaf") in {39}:
        # receiver.TransferFactorToSoilConiferousLeaf(chem)

        print(">>>>>>>>>>>>> TransferFractionToSoilTotalConiferousLeaf (self.transferfractionleaf) <<<<<<<<<<<<<<<<")
        transferfractionleaf = receiver.TransferFractionToSoilTotalConiferousLeaf(chem)
        print(receiver.parameters.get("TransferFractionToSoilTotalConiferousLeaf").formula.equation)
        print(f"\t= {transferfractionleaf}")

        print("\n\n")

        print(">>>>>>>>>>>>> TransferFractionToSoilSoil (self.transferfractionsoil) <<<<<<<<<<<<<<<<")
        transferfractionsoil = receiver.TransferFractionToSoilSoil(chem)
        print(receiver.parameters.get("TransferFractionToSoilSoil").formula.equation)
        print(f"\t= {transferfractionsoil}")
    else:
        1


if __name__ == "__main__":
    equation_check_1()
    equation_check_2()
    equation_check_1()
