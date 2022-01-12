from ..schema.scenarios.models import *
from .generic import GenericService
from .parameters import parameterize

__all__ = ['ScenarioService']


class ScenarioService(GenericService):
    __model__ = parameterize(Scenario)
