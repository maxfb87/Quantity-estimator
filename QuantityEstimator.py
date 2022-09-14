from blenderbim.bim.module.pset.qto_calculator import QtoCalculator
from blenderbim.bim.module.pset.data import ObjectQtosData
from ifcopenshell.api.pset.data import Data
from blenderbim.bim.ifc import IfcStore
import ifcopenshell.api
import bpy

objects = bpy.context.selected_objects

for object in objects:
    bpy.context.view_layer.objects.active = object

    ObjectQtosData.load()
    pset_qtos = ObjectQtosData.data["qtos"]

    if not pset_qtos:
        print("There are no pset quantities")
        continue

    for pset_qto in pset_qtos:
        print(pset_qto)
        defined_quantities = pset_qto['Properties']
        for quantity in defined_quantities:
            quantity_name = quantity['Name']
            alternative_prop_names = [p['Name'] for p in pset_qto['Properties']]

            calculator = QtoCalculator()
            new_quantity = calculator.guess_quantity(quantity_name, alternative_prop_names, object)

            new_quantity = round(new_quantity, 3)

            file = IfcStore.get_file()
            pset_qto_id= file.by_id(pset_qto['id'])
            pset_qto_name = pset_qto['Name']

            ifcopenshell.api.run("pset.edit_qto",
                file,
                **{"qto" : pset_qto_id, "name" : pset_qto_name, "properties": {quantity_name : new_quantity}}
            )

            ObjectQtosData.load()

            ifc_definition_id = object.BIMObjectProperties.ifc_definition_id

            Data.load(file, ifc_definition_id)

