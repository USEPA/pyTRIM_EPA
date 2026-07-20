import pandas as pd
from ..schema.entities.models import *
from ..schema.entities.environment import DummyLink
from ..schema.utils.caching import CacheManager
from .generic import GenericService
from .parameters import parameterize
from .utils import classproperty

__all__ = [
    'ChemicalService',
    'ParcelService', 'VolumeElementService', 'CompartmentService',
    'TransportProcessService'
]


class ChemicalService(GenericService[Chemical]):
    __model__ = parameterize(
        Chemical,
        # at the moment chemicals take custom params from the Foundries/Default scenario
        globalize_custom_parameters=True,
        default_scenario=lambda x: x._scenarios[0]
    )

    @classproperty
    def mercury_transformation_parameters(cls):
        return {
            'Divalent Mercury': ['MethylationRate', 'ReductionRate'],
            'Elemental Mercury': ['OxidationRate'],
            'MethylMercury': ['DemethylationRate']
        }

    @classmethod
    def get_mercury_transformation_rates(cls, parcel):
        mercuries = parcel.scenario.get_chemicals(category='Mercury')
        if not mercuries:
            raise AssertionError('Scenario Does Not Include Mercury Emissions')

        def safe_eval(chem, comp, param_name):
            try:
                val = getattr(chem, param_name)(comp)
                if not pd.isna(val):
                    return val
            except Exception:
                pass
            return None

        target_rates = dict(cls.mercury_transformation_parameters)

        def media_key(comp):
            if comp.media.isa('Surface_Soil'):
                return 'Surface_Soil'
            return comp.media.name

        mtr_params = {}
        for comp in parcel.compartments:
            if not (
                comp.media.isa('Air')
                or comp.media.isa('Soil')
                or comp.media.isa('Groundwater')
                or comp.media.isa('Surface_Water')
                or comp.media.isa('Sediment')
            ):
                continue
            key = media_key(comp)
            mtr_params[key] = {chem_name: {} for chem_name in target_rates}
            media_params = mtr_params[key]
            for chem in mercuries:
                for rate in target_rates[chem.name]:
                    try:
                        v = safe_eval(chem, comp, rate)
                        if v is not None:
                            # print(f'Got {rate}="{v}" for {chem} from {comp}')
                            media_params[chem.name][rate] = v
                    except Exception:
                        pass
        return mtr_params

    @classmethod
    def update_mercury_transformation_rate(
        cls, parcel, rate_name, media_type, value, unit='1/day'
    ):
        # print(f'Set {parcel}[{rate_name}] = "{value} {unit}" for "{media_type}"')
        param_map = dict(cls.mercury_transformation_parameters)
        comps = parcel.get_compartment(media=media_type)
        if not comps:
            return
        for chem_name, rates in param_map.items():
            if rate_name not in rates:
                continue
            chem = cls.get(name=chem_name)
            chem.current_scenario(parcel.scenario)
            if not chem:
                continue  # Shouldn't happen, but still...
            for compartment in comps:
                formula = f'({value}) if compartment.id in {{{compartment.id}}} else 0'
                chem.parameters.set(rate_name, formula=formula, unit=unit)
                # cp = chem.parameters.get(rate_name)
                # print(f'Got {parcel}[{rate_name}] = "{cp}" ({cp.formula.eval(compartment)})')
        ChemicalService.commit()


class ParcelService(GenericService[Parcel]):
    __model__ = Parcel


class VolumeElementService(GenericService[VolumeElement]):
    __model__ = parameterize(
        VolumeElement,
        default_scenario=lambda x: x.parcel.scenario
    )


class CompartmentService(GenericService[Compartment]):
    __model__ = parameterize(
        Compartment,
        default_scenario=lambda x: x.volume_element.parcel.scenario
    )

    class media(GenericService[Media]):
        __model__ = Media

        @classmethod
        def create(
            cls, *, category=None,
            no_commit=False, check_unique=True, **kwargs
        ):
            if category is not None:
                m = None
                for name in category.split('|'):
                    parent = m
                    m = cls.get_or_create(
                        name=name,
                        no_commit=True
                    )
                    if m.parent_id is None and parent:
                        m.parent = parent
                if not no_commit:
                    cls.commit()
                return m
            else:
                return super().create(
                    no_commit=no_commit, check_unique=check_unique, **kwargs
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

    class links(GenericService[CompartmentLink]):
        __model__ = CompartmentLink


class TransportProcessService(GenericService[TransportProcess]):
    __model__ = TransportProcess


@CacheManager.with_caching('link-tps')
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
