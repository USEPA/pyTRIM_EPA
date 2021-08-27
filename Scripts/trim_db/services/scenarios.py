from ..schema.scenarios.models import *
from .generic import GenericService

__all__ = ['ScenarioService']


class ScenarioService(GenericService):
    __model__ = Scenario
