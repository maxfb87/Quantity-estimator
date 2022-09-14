from ifcopenshell import util
from blenderbim.bim.module.pset.qto_calculator import QtoCalculator
import ifcopenshell
from blenderbim.bim.ifc import IfcStore
import bpy

selected_objects = bpy.context.selected_objects

ifc = ifcopenshell.open(IfcStore.path)

calculator = QtoCalculator()

pset_qto = util.pset.PsetQto('IFC4')
print('\n')

for object in selected_objects:
    bpy.context.view_layer.objects.active = object

    object_ifc_id = object.BIMObjectProperties.ifc_definition_id
    ifc_object_instance = ifc.by_id(object_ifc_id)

    pset_qto_ifc_instances = ifcopenshell.util.element.get_psets(ifc_object_instance, qtos_only = True)

    if not pset_qto_ifc_instances:
        continue

    ifc_object_type = ifc_object_instance.get_info()['type']

    applicable_pset_names = pset_qto.get_applicable_names(ifc_object_type)

    print(applicable_pset_names)

    for applicable_pset_name in applicable_pset_names:
        if 'Qto_' in applicable_pset_name:
            pset_qto_name = applicable_pset_name

    pset_qto_properties = pset_qto.get_by_name(pset_qto_name).get_info()['HasPropertyTemplates']

    for pset_qto_property in pset_qto_properties:
        print(pset_qto_property.get_info()['Name'])
        quantity_name = pset_qto_property.get_info()['Name']
        #TODO add alternative prop name

        new_quantity = calculator.guess_quantity(quantity_name, quantity_name, object)

        if not new_quantity:
            new_quantity = 0
        else:
            new_quantity = round(new_quantity, 3)

        file = IfcStore.get_file() #TODO check if can be used ifc variable defined before


        pset_qto_id = file.by_id(pset_qto_ifc_instances[pset_qto_name]['id']) #TODO check if i can use line above

        ifcopenshell.api.run("pset.edit_qto",
                file,
                **{"qto" : pset_qto_id, "name" : pset_qto_name, "properties": {quantity_name : new_quantity}}
            )



