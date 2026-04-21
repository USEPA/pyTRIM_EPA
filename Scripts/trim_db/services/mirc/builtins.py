from ...schema.mirc.builtins.models import *
from ..generic import GenericService

__all__ = ['MircProductService', 'MircLifeStageService', 'MircPercentileService']


class MircProductService(GenericService):
    __model__ = MircProduct


class MircLifeStageService(GenericService):
    __model__ = MircLifeStage


class MircPercentileService(GenericService):
    __model__ = MircPercentile
