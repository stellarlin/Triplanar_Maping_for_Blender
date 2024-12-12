import bpy

from . import triplanar_properties as properties

class PlanarMapping_Panel(bpy.types.Panel):
    bl_label = "Triplanar Mapping"
    bl_idname = "TRIPLANE_MAPPING_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Triplanar Mapping Panel"

    def draw_tex_image(self, layout, prop):
        # Display properties in the UI
        layout.prop(prop, "name")
        layout.prop(prop, "texture")
        layout.prop(prop, "scale")
        layout.prop(prop, "blending")


    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Block 1: Create Material Section
        layout.label(text="Create a New Material:")
        layout.prop(scene, "texture_type")

        if scene.texture_type == 'TEX_IMAGE':
            self.draw_tex_image(layout, scene.image_properties)

        if scene.texture_type != 'NONE':
            layout.operator("material.apply_planar")
            layout.operator("material.update_planar")