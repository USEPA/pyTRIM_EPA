from trim_db.services import ScenarioService

TRIM_FILES = (
    'C:/Users/50466/Documents/Projects/sandbox/TRIM/'
    'trim-builder/Scripts/trim_core/backend/Input_Files'
)


def get_dummy_user():
    from trim_db.schema import Model, RoleMixin, UserMixin
    from trim_db.services.generic import GenericService

    class Role(RoleMixin, Model):
        pass

    class User(UserMixin, Model):
        pass

    class UserService(GenericService):
        __model__ = User

    return UserService.get_or_create(email='tester@test.org')


def import_ve(scenario, filepaths):
    from trim_db.porting.volume_elements import parse_volume_elements

    for filepath in filepaths:
        vols = parse_volume_elements(filepath)
        ScenarioService(scenario).add_volumes(vols)

    # ScenarioService.commit()


def import_master_library(scenario, master_filepath, props_filepath):
    from trim_db.porting.master_library import parse_master_library

    parse_master_library(
        TRIM_FILES, scenario, master_filepath, props_filepath
    )

    # ScenarioService.commit()


def demo_print(scenario):
    # from pprint import pprint

    # from trim_db.services import VolumeElementService
    # pprint({
    #     model.name: model
    #     for model in VolumeElementService.get_all()
    # })

    # from trim_db.services import ChemicalService
    # pprint({
    #     model.name: model
    #     for model in ChemicalService.get_all()
    # })

    # print(scenario.parameters)

    from itertools import combinations

    print('')
    with scenario.global_environment() as env:
        print(env)
        print(f'\tIdealGasConstant = {env.IdealGasConstant}')
        print(f'\tAirTemperature_K = {env.AirTemperature_K}')
        print('')

        vols = []

        for vol in env.volume_elements:
            if 'Air_E1' not in vol.name:
                continue
            vols.append(vol)
            print(vol)
            print(f'\ttop = {vol.top}')
            print(f'\tbottom = {vol.bottom}')
            # print(vol.parameters)
            for comp in vol.compartments:
                print(f'  > {comp}')
                print(f'    ("{comp.full_name}")')
                print(f'\tDustLoad = {comp.DustLoad}')
                print(f'\tDustDensity = {comp.DustDensity}')
                # print(comp.parameters)
            print('')

        for (a, b) in combinations(vols, 2):
            print(f'"{a.name}" U "{b.name}" = {a.overlap_with(b)}')
        print('')

        for chem in env.chemicals:
            if 'Mercury' not in chem.category:
                continue
            print(chem)
            # print(chem.parameters)
            print(f'\tHenryLawConstant = {chem.HenryLawConstant}')
            print(f'\tZ_purewater = {chem.Z_purewater}')
            print(f'\tH_over_R_T = {chem.H_over_R_T}')
            print('')


if __name__ == '__main__':
    u = get_dummy_user()
    scenario = ScenarioService.get_or_create(name='Lorem Ipsum', creator=u)

    import_ve(
        scenario,
        [
            f'{TRIM_FILES}/Foundries_SS (2) Volume Elements.txt',
            f'{TRIM_FILES}/Foundries_SS_2_pseudo_volume_elements.txt'
        ]
    )

    import_master_library(
        scenario,
        f'{TRIM_FILES}/ICF_Master_Library_03212016_PropertyExporter.txt',
        f'{TRIM_FILES}/Foundries_SS (4) Properties.txt'
    )

    demo_print(scenario)
