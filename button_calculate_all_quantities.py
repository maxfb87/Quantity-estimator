from ifcopenshell import util
import ifcopenshell
from blenderbim.bim.ifc import IfcStore
import bpy

objects = bpy.context.selected_objects

ifc = ifcopenshell.open(IfcStore.path)

pset_qto = util.pset.PsetQto('IFC4')
print('\n')

for object in objects:
    bpy.context.view_layer.objects.active = object

    object_id = object.BIMObjectProperties.ifc_definition_id
    ifc_object = ifc.by_id(object_id)

    object_type = ifc_object.get_info()['type']

    applicable_names = pset_qto.get_applicable_names(object_type)

    for applicable_name in applicable_names:
        if 'Qto_' in applicable_name:
            qto_property_name = applicable_name

    qto_properties = pset_qto.get_by_name(qto_property_name).get_info()['HasPropertyTemplates']
    #name = pset_qto.get_by_name('Qto_WallBaseQuantities').get_info()['HasPropertyTemplates'][1].get_info()['Name']

    for qto_property in qto_properties:
        print(qto_property.get_info()['Name'])


