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
    qtos = ObjectQtosData.data["qtos"]
    
    if not qtos:
        print("There are no quantities")
        continue
    
    for qto in qtos:
        defined_quantities = qto['Properties']
        for quantity in defined_quantities:
            quantity_name = quantity['Name']
            alternative_prop_names = [p['Name'] for p in qto['Properties']]
            
            calculator = QtoCalculator()
            new_quantity = calculator.guess_quantity(quantity_name, alternative_prop_names, object)
            
            new_quantity = round(new_quantity, 3)
            
            file = IfcStore.get_file()
            qto_id = file.by_id(qto['id'])
            qto_name = qto['Name']
            
            ifcopenshell.api.run("pset.edit_qto",
                file,
                **{"qto" : qto_id, "name" : qto_name, "properties": {quantity_name : new_quantity}}
            )

            ObjectQtosData.load()

            ifc_definition_id = object.BIMObjectProperties.ifc_definition_id
            
            Data.load(file, ifc_definition_id)

