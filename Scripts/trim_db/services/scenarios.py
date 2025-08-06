from ..schema.scenarios.models import *
from .generic import GenericService
from .parameters import parameterize

__all__ = ['ScenarioService']


class ScenarioService(GenericService):
    __model__ = parameterize(Scenario)

    @classmethod
    def get_surface_runoff(cls, scen):
        soil_comps = []
        water_comps = []
        sink_comps = []
        for c in scen.compartments:
            if c.media.isa('Surface_Soil'):
                soil_comps.append(c)
            elif c.media.isa('Surface_Water'):
                water_comps.append(c)
            elif (c.media.isa("Advection") & (not c.media.isa("Flush$"))):
                sink_comps.append(c)
        runoffs = {}
        for send in soil_comps + water_comps:
            sending_parcel = send.volume_element.parcel.name
            runoffs[sending_parcel] = {}
            runoffs[sending_parcel]['sink'] = 0
            for recv in soil_comps + sink_comps + water_comps:
                receiving_parcel = recv.volume_element.parcel.name
                if send in water_comps:
                    if send == recv:
                        runoffs[sending_parcel][receiving_parcel] = 1
                    else:
                        runoffs[sending_parcel][receiving_parcel] = 0
                    continue
                if recv in sink_comps:
                    runoffs[sending_parcel]['sink'] += send.FractionOfTotalRunoff(receiver=recv)
                else:
                    runoffs[sending_parcel][receiving_parcel] = send.FractionOfTotalRunoff(receiver=recv)
        return runoffs
