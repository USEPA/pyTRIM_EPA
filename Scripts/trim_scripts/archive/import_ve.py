from trim_db.porting.environment import parse_volume_elements
from trim_db.services import ScenarioService, VolumeElementService

from trim_db.schema import Model, RoleMixin, UserMixin
from trim_db.services.generic import GenericService


class Role(RoleMixin, Model):
    pass


class User(UserMixin, Model):
    pass


class UserService(GenericService):
    __model__ = User


def import_ve(filepath):
    u = UserService.get_or_create(email='tester@test.org')
    s = ScenarioService.get_or_create(name='Lorem Ipsum', creator=u)

    vols = parse_volume_elements(s.id, filepath)
    VolumeElementService.update(vols)

    from pprint import pprint
    pprint(VolumeElementService.get_all())


if __name__ == '__main__':
    import_ve(
        'C:/Users/50466/Documents/Projects/sandbox/TRIM/'
        'trim-builder/Scripts/trim_core/backend/Input_Files/'
        'Foundries_SS (2) Volume Elements.txt'
    )
