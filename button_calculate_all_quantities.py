import ifcopenshell
import bpy
from blenderbim.bim.module.pset.qto_calculator import QtoCalculator
from blenderbim.bim.ifc import IfcStore
from ifcopenshell import util


class qtoAllQuantitiesCalculator():

    def __init__(self):
        self.file = IfcStore.get_file()
        self.calculator = QtoCalculator()
        self.pset_qto = util.pset.PsetQto('IFC4')

    def calculate_all_qtos(self, selected_objects):

        for object in selected_objects:

            self.set_active_object(object)

            self.pset_qto_object_ifc_instance = self.get_pset_qto_object_ifc_instance(object)

            if not self.pset_qto_object_ifc_instance:
                print("There is no pset qto instance associated to object " + object.name)
                continue

            self.pset_qto_properties = self.get_pset_qto_properties(object)

            for pset_qto_property in self.pset_qto_properties:
                quantity_name = pset_qto_property.get_info()['Name']
                #TODO add alternative prop name option

                new_quantity = self.calculator.guess_quantity(quantity_name, quantity_name, object)

                if not new_quantity:
                    new_quantity = 0
                else:
                    new_quantity = round(new_quantity, 3)

                #TODO Check if pset_qto_name can be global

                self.edit_qto(object, quantity_name, new_quantity)


    def set_active_object(self, object):
        bpy.context.view_layer.objects.active = object

    def get_ifc_object_instance(self, object):
        object_ifc_id = object.BIMObjectProperties.ifc_definition_id
        ifc_object_instance = self.file.by_id(object_ifc_id)
        return ifc_object_instance

    def get_pset_qto_object_ifc_instance(self, object):
        ifc_object_instance = self.get_ifc_object_instance(object)
        pset_qto_ifc_instance = ifcopenshell.util.element.get_psets(ifc_object_instance, qtos_only = True)
        return pset_qto_ifc_instance

    def get_pset_qto_properties(self, object):
        pset_qto_name = self.get_pset_qto_name(object)
        pset_qto_properties = self.pset_qto.get_by_name(pset_qto_name).get_info()['HasPropertyTemplates']
        return pset_qto_properties

    def get_applicable_pset_names(self, object):
        ifc_object_instance = self.get_ifc_object_instance(object)
        ifc_object_type = ifc_object_instance.get_info()['type']
        applicable_pset_names = self.pset_qto.get_applicable_names(ifc_object_type)
        return applicable_pset_names

    def get_pset_qto_name(self, object):
        applicable_pset_names = self.get_applicable_pset_names(object)
        for applicable_pset_name in applicable_pset_names:
            if 'Qto_' in applicable_pset_name:
                pset_qto_name = applicable_pset_name
                return pset_qto_name

    def get_pset_qto_id(self, object):
        pset_qto_name = self.get_pset_qto_name(object)
        pset_qto_id = self.file.by_id(self.pset_qto_object_ifc_instance[pset_qto_name]['id']) #TODO check if i can use line above
        return pset_qto_id

    def edit_qto(self, object, quantity_name, new_quantity):
        pset_qto_name = self.get_pset_qto_name(object)
        pset_qto_id = self.get_pset_qto_id(object)

        ifcopenshell.api.run("pset.edit_qto",
                self.file,
                **{"qto" : pset_qto_id, "name" : pset_qto_name, "properties": {quantity_name : new_quantity}}
            )

qto_all_quantities_calculator = qtoAllQuantitiesCalculator()

qto_all_quantities_calculator.calculate_all_qtos(selected_objects = bpy.context.selected_objects)
