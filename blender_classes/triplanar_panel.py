import bpy


class TriplanarPanel(bpy.types.Panel):
    bl_label = "Triplanar Mapping"
    bl_idname = "TRIPLANE_MAPPING_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Triplane Texture"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        triplanar_properties = scene.triplanar_properties

        # Texture Inputs for X, Y, and Z axes
        layout.prop(triplanar_properties, "texture_x")
        layout.prop(triplanar_properties, "texture_y")
        layout.prop(triplanar_properties, "texture_z")

        # Scale input for triplanar mapping
        layout.prop(triplanar_properties, "scale")

        # Name of the material
        layout.prop(triplanar_properties, "name")

        # Button to apply triplanar mapping
        layout.operator("object.apply_triplanar_mapping", text="Apply Triplanar Mapping")


