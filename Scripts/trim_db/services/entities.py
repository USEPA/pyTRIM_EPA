from ..schema.entities.models import *
from ..schema.entities.environment import DummyLink
from ..schema.utils.caching import with_cache
from .generic import GenericService
from .parameters import parameterize

__all__ = [
    'ChemicalService',
    'ParcelService', 'VolumeElementService', 'CompartmentService',
    'TransportProcessService'
]


class ChemicalService(GenericService):
    __model__ = parameterize(Chemical)


class ParcelService(GenericService):
    __model__ = Parcel


class VolumeElementService(GenericService):
    __model__ = parameterize(VolumeElement)


class CompartmentService(GenericService):
    __model__ = parameterize(Compartment)

    class media(GenericService):
        __model__ = Media

        @classmethod
        def create(
            cls, *, category=None,
            no_commit=False, check_unique=True, **kwargs
        ):
            if category is not None:
                m = None
                for name in category.split('|'):
                    m = cls.get_or_create(
                        name=name,
                        parent_id=m.id if m is not None else None
                    )
                return m
            else:
                return super().create(
                    no_commit=False, check_unique=True, **kwargs
                )

        @classmethod
        def get(cls, model_id=None, category=None, **kwargs):
            if model_id is None and category is not None:
                m = [
                    x for x in cls.get_all(**kwargs) if x.category == category
                ]
                if m:
                    return m[0]
                return None
            else:
                return super().get(model_id=model_id, **kwargs)

    class links(GenericService):
        __model__ = CompartmentLink


class TransportProcessService(GenericService):
    __model__ = TransportProcess


@with_cache('link-tps::')
def get_transport_processes(link, chemical):
    tfs = TransportProcessService.get_all()
    s = link.sender
    r = link.receiver
    if s != r:
        tfs = [x for x in tfs if not x.is_transform]
    tfs = [x for x in tfs if x.applies_to(
        sender=s, receiver=r, chemical=chemical
    )]
    return tfs


setattr(CompartmentLink, 'transport_processes', get_transport_processes)
setattr(DummyLink, 'transport_processes', get_transport_processes)
