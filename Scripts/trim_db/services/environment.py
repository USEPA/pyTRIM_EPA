from ..schema.environment.models import *
from .generic import GenericService

__all__ = ['VolumeElementService']


class VolumeElementService(GenericService):
    __model__ = VolumeElement
