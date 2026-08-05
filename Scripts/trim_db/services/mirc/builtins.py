import enum
from ...schema.mirc.builtins.models import *
from ..generic import GenericService

__all__ = ['MircProductService', 'MircLifeStageService', 'MircPercentileService']


class MircProductService(GenericService[MircProduct]):
    __model__ = MircProduct


class AgeOrder(enum.Enum):
    CHILD_LESS_THAN_1 = 0
    CHILD_1_2 = 10
    CHILD_3_5 = 20
    CHILD_6_11 = 30
    CHILD_12_19 = 40
    ADULT = 50
    PREGNANT_MOTHER = 55


class MircLifeStageService(GenericService[MircLifeStage]):
    __model__ = MircLifeStage

    @classmethod
    def as_orderable(cls, life_stage):
        norm_name = life_stage.name.upper()
        norm_name = norm_name.replace(' ', '_').replace('-', '_').replace('<', 'LESS_THAN_')
        return AgeOrder[norm_name].value


class MircPercentileService(GenericService[MircPercentile]):
    __model__ = MircPercentile
