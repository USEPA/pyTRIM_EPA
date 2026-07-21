import sqlalchemy as sa
from ..parameters.managers import ParameterManager
from ...utils.base import Model
from ...utils.serialize import register_serializer


__all__ = [
    'MircProduct', 'MircLifeStage', 'MircPercentile'
]


PRIORITY_CHEMICALS = [
    '7440-38-2',  # Arsenic Compounds
    '7440-43-9',  # Cadmium Compounds
    '22967-92-6',  # Methyl Mercury
    '7487-94-7',  # Divalent Mercury (Mercuric chloride),
    '7439-97-6',  # Elemental Mercury (Mercury)
    # Dioxins
    '39001-02-0',  # 1,2,3,4,6,7,8,9-Octochlorodibenzofuran
    '3268-87-9',  # 1,2,3,4,6,7,8,9-Octochlorodibenzo-p-dioxin
    '67562-39-4',  # 1,2,3,4,6,7,8-Heptachlorodibenzofuran
    '35822-46-9',  # 1,2,3,4,6,7,8-Heptachlorodibenzo-p-dioxin
    '55673-89-7',  # 1,2,3,4,7,8,9-Heptachlorodibenzofuran
    '70648-26-9',  # 1,2,3,4,7,8-Hexachlorodibenzofuran
    '39227-28-6',  # 1,2,3,4,7,8-Hexachlorodibenzo-p-dioxin
    '57117-44-9',  # 1,2,3,6,7,8-Hexachlorodibenzofuran
    '57653-85-7',  # 1,2,3,6,7,8-Hexachlorodibenzo-p-dioxin
    '72918-21-9',  # 1,2,3,7,8,9-Hexachlorodibenzofuran
    '19408-74-3',  # 1,2,3,7,8,9-Hexachlorodibenzo-p-dioxin
    '57117-41-6',  # 1,2,3,7,8-Pentachlorodibenzofuran
    '40321-76-4',  # 1,2,3,7,8-Pentachlorodibenzo-p-dioxin
    '60851-34-5',  # 2,3,4,6,7,8-Hexachlorodibenzofuran
    '57117-31-4',  # 2,3,4,7,8-Pentachlorodibenzofuran
    '51207-31-9',  # 2,3,7,8-Tetrachlorodibenzofuran
    '1746-01-6',  # 2,3,7,8-Tetrachlorodibenzo-p-dioxin
    # POM/PAHs
    '91-57-6',  # 2-Methylnaphthalene
    '57-97-6',  # 7,12-Dimethylbenz[a]Anthracene
    '83-32-9',  # Acenaphthene
    '208-96-8',  # Acenaphthylene
    '56-55-3',  # Benz[a]Anthracene
    '191-24-2',  # Benzo(ghi)perylene
    '50-32-8',  # Benzo[a]Pyrene
    '205-99-2',  # Benzo[b]Fluoranthene
    '207-08-9',  # Benzo[k]Fluoranthene
    '218-01-9',  # Chrysene
    '53-70-3',  # Dibenzo[a,h]Anthracene
    '206-44-0',  # Fluoranthene
    '86-73-7',  # Fluorene
    '193-39-5',  # Indeno[1,2,3-c,d]Pyrene
]


class NamedModelMixin:
    name = sa.Column(sa.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.__class__.__qualname__}('{self.name}')"


class MircProduct(NamedModelMixin, Model):
    """Represents a specific product which is ingested
    by human or animal consumers.
    """
    category_id = sa.Column(
        sa.Integer(),
        sa.ForeignKey('mirc_product.id'),
        nullable=True
    )
    category = sa.orm.relationship(
        'MircProduct', remote_side='MircProduct.id',
        backref=sa.orm.backref("subcategories", cascade='all, delete-orphan')
    )

    is_food = sa.Column(sa.Boolean(), nullable=False, default=False)
    is_feed = sa.Column(sa.Boolean(), nullable=False, default=False)

    def is_a(self, name, strict=False):
        if self.name == name:
            return True

        if not strict and self.category:
            return self.category.is_a(name)

        return False

    def get_parameters(self, scenario):
        return ParameterManager(scenario).for_product(self)


@register_serializer(MircProduct)
def _ts_product(p: MircProduct):
    serial = {
        'id': p.id,
        'name': p.name
    }
    if p.category:
        serial['category'] = p.category.name
    subcategories = [sub.name for sub in p.subcategories]
    if subcategories:
        serial['subcategories'] = subcategories
    return serial


class MircLifeStage(NamedModelMixin, Model):
    """Represents an age group (i.e., "Adult").
    """
    duration = sa.Column(sa.Float())
    duration_unit = sa.Column(sa.String(255))


@register_serializer(MircLifeStage)
def _ts_life_stage(ls: MircLifeStage):
    return {
        'id': ls.id,
        'name': ls.name,
        'duration': ls.duration,
        'duration_unit': ls.duration_unit
    }


class MircPercentile(NamedModelMixin, Model):
    """Represents a targeted portion of a study population.
    """
    pass


@register_serializer(MircPercentile)
def _ts_percentile(pct: MircPercentile):
    return {
        'id': pct.id,
        'name': pct.name
    }
