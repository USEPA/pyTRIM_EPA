from ..schema.scenarios.models import *
from ..schema.environment.models import VolumeElement
from .generic import GenericService

__all__ = ['ScenarioService']


class ScenarioService(GenericService):
    __model__ = Scenario

    def __init__(self, scenario):
        self._scenario = scenario

    def add_volumes(self, vols):
        for vol in vols:
            if len([
                x for x in self._scenario.parcels
                if x.name == vol.parcel.name
            ]):
                continue
            self._scenario.parcels.append(vol.parcel)


class EnvironmentManager:
    def __init__(self, scenario):
        self._scenario = scenario

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    @property
    def parameters(self):
        return self._scenario.parameters

    def __getattr__(self, name):
        param = getattr(self.parameters, name)
        if param is None:
            return None
        if param.quantity:
            return param.quantity
        elif param.equation:
            return param.equation(self._scenario)
        else:
            raise AttributeError(name)

    @property
    def ManagedEntity(self):
        class Entity:
            def __init__(s, model):
                s._managed_model = model

            @property
            def compartments(s):
                if not isinstance(s._managed_model, VolumeElement):
                    raise AttributeError('compartments')
                return [
                    self.ManagedEntity(x)
                    for x in s._managed_model.compartments
                ]

            def get_compartment(s, name):
                if not isinstance(s._managed_model, VolumeElement):
                    raise AttributeError('get_compartment')
                comp = s._managed_model.get_compartment(name)
                if comp is None:
                    return None
                return self.ManagedEntity(comp)

            @property
            def parameters(s):
                return s._managed_model.parameters(self._scenario)

            def __getattr__(s, name):
                try:
                    return getattr(s._managed_model, name)
                except AttributeError:
                    param = getattr(s.parameters, name)
                    if param is None:
                        return None
                    if param.quantity:
                        return param.quantity
                    elif param.equation:
                        return param.equation(self._scenario)
                    else:
                        raise

            def __repr__(s):
                return f'Managed({repr(s._managed_model)})'

        return Entity

    @property
    def chemicals(self):
        return [self.ManagedEntity(x) for x in self._scenario.chemicals]

    @property
    def volume_elements(self):
        return [self.ManagedEntity(x) for x in self._scenario.volume_elements]

    def get_volume_element(self, name):
        for x in self.volume_elements:
            if x.name == name:
                return x
        return None

    def __repr__(self):
        return f'EnvironmentManager({self._scenario})'


Scenario.global_environment = lambda s: EnvironmentManager(s)
