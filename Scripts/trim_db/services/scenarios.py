from ..schema.utils.caching import CacheManager
from ..schema.scenarios.models import *
from .generic import GenericService
from .parameters import parameterize

__all__ = ['ScenarioService']


class ScenarioService(GenericService):
    __model__ = parameterize(Scenario)

    def __init__(self, model, *args, **kwargs):
        self.__instance = model

    def get_surface_runoff(self):
        return get_scenario_surface_runoff(self.__instance)


@CacheManager.with_caching('surface_runoff')
def get_scenario_surface_runoff(scen):
    soil_comps = []
    water_comps = []
    sink_comps = []
    for c in scen.compartments:
        if c.media.isa('Surface_Soil'):
            soil_comps.append(c)
        elif c.media.isa('Surface_Water'):
            water_comps.append(c)
        elif (c.media.isa("Advection") and not c.media.isa("Flush$")):
            sink_comps.append(c)
    runoffs = {}
    for sender in soil_comps + water_comps:
        sending_parcel = sender.volume_element.parcel.name
        runoffs[sending_parcel] = {}
        runoffs[sending_parcel]['sink'] = 0
        for receiver in soil_comps + sink_comps + water_comps:
            receiving_parcel = receiver.volume_element.parcel.name
            if sender in water_comps:
                if sender == receiver:
                    runoffs[sending_parcel][receiving_parcel] = 1
                else:
                    runoffs[sending_parcel][receiving_parcel] = 0
                continue
            runoff_frac = sender.FractionOfTotalRunoff(receiver=receiver)
            if receiver in sink_comps:
                runoffs[sending_parcel]['sink'] += runoff_frac
            else:
                runoffs[sending_parcel][receiving_parcel] = runoff_frac
    return runoffs
