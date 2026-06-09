from ...schema.mirc.builtins.models import *
from ..generic import GenericService

__all__ = ['MircProductService', 'MircLifeStageService', 'MircPercentileService']


class MircProductService(GenericService[MircProduct]):
    __model__ = MircProduct


class MircLifeStageService(GenericService[MircLifeStage]):
    __model__ = MircLifeStage


class MircPercentileService(GenericService[MircPercentile]):
    __model__ = MircPercentile
