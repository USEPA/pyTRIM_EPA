from ..schema.chemicals.models import *
from .generic import GenericService

__all__ = ['ChemicalService']


class ChemicalService(GenericService):
    __model__ = Chemical
