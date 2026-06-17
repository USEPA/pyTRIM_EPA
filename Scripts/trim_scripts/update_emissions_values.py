from base import *

from trim_frontend.parcels.utils import handle_parcel_update

"""
Script for updating dry/wet particle/vapor source
based on .csv input

Sample payload
{
    'chemical_name': 'MethylMercury',
    'compartment_name': 'DryVaporSource',
    'emission_value': '1',
    'field': 'emission',
    'id': '2852',
    've_name': 'DryVaporSource'
}
"""


def update_emissions_values(scenario_id, scenario_name, csv_fp):
    df = pd.read_csv(csv_fp)
    emissions_data = df.set_index("Parcel").to_dict(orient="index")

    scenario_id = scenario_id
    scen = ScenarioService.get(scenario_id)
    assert scen.name == scenario_name

    for chem in scen.chemicals:
        for pcl in scen.parcels:
            emission = emissions_data[pcl.name]
            for name, value in emission.items():
                payload = {
                    "chemical_name": chem.name,
                    "compartment_name": name,
                    "emission_value": value,
                    "field": "emission",
                    "id": pcl.id,
                    "ve_name": name,
                }
                handle_parcel_update(pcl, payload)


if __name__ == "__main__":
    try:
        update_emissions_values(
            scenario_id=153,
            scenario_name="Tier1_Congeners",
            csv_fp=r"C:\Users\55586\Desktop\tools\trim\scripts\Tier1_Congeners_Emissions.csv",
        )
    except Exception as e:
        traceback.print_exc()
    print("!")
