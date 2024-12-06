import bpy

class PlanarMapping_Panel(bpy.types.Panel):
    bl_label = "Triplanar Mapping"
    bl_idname = "TRIPLANE_MAPPING_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Triplanar Mapping Panel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        prop = scene.planar_properties

        # Block 1: Create Material Section
        layout.label(text="Create a New Material:")

        if prop:
            # Display properties in the UI
            layout.prop(prop, "texture")
            layout.prop(prop, "scale")
            layout.prop(prop, "blending")
            layout.prop(prop, "name")

            # Button to create material
            layout.operator("material.apply_planar")
        else:
            self.report({'ERROR'}, "No props")

 #       layout.separator()  # Add a separator between blocks
 #       layout.label(text="Apply Existing Material:")

        # Block 2: Apply Material from Global List
        # List available materials
      #  layout.label(text="Available Materials:")
     #   for mat in bpy.data.materials:
      #      row = layout.row()
      #      row.label(text=mat.name)
      #      # Example of adding a button to assign material to the active object
      #      row.operator("object.apply_material", text="Apply").material = mat
#

