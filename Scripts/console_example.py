from trim_db.local import *
from trim_db.services import *

s = ScenarioService.get(name='Foundries_SS')
s

chem = ChemicalService.get(name='Divalent Mercury')
chem

v1 = s.get_volume_element('VadoseSoil_E1')
v1

v2 = s.get_volume_element('GW_E2')
v2

c1 = v1.get_compartment(media='Vadose_Zone')[0]
c1

c2 = v2.get_compartment(media='Groundwater')[0]
c2

link = c1.get_links(c2)[0]
tps = link.transport_processes(chem)

tp = tps[0]
tp.name
tp.applies_to(sender=c1, receiver=c2, chemical=chem)

c1.CustomVolume

tp.eval(environment=s, chemical=chem, sender=c1, receiver=c2)




v = s.get_volume_element('SurfSoil_E1')
v

v.parcel.area

v.height
v.area
v.volume
v.height * v.area == v.volume

c = v.get_compartment(media='Grass_Leaf')[0]
c

c.CustomHeight
c.CustomArea
c.CustomVolume

c.height
c.area
c.volume
c.height * c.area == c.volume

c.height == v.height
c.area == v.area
c.volume == v.volume

# c.VolumeFraction_Vapor
