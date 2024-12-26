import bpy


class PlanarMappingPanel(bpy.types.Panel):
    bl_label = "Triplanar Mapping"
    bl_idname = "TRIPLANE_MAPPING_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Triplanar Mapping Panel"

    def draw_tex_image(self, layout, prop):
        # Display properties in the UI
        layout.prop(prop, "name")
        layout.prop(prop, "texture")
        layout.prop(prop, "mapping_scale")
        layout.prop(prop, "blending")

    def draw_colors(self, layout,prop):
        # Color-position pairs
        box = layout.box()
        box.label(text="Colors:")
        for i in range(1, 5):
            color_pair_attr = f"color_pair_{i}"
            if hasattr(prop, color_pair_attr):
                color_pair = getattr(prop, color_pair_attr)

                # Display Color and Position for each pair
                row = box.row()
                row.prop(color_pair, "color", text=f"Color {i}")
                row.prop(color_pair, "position", text=f"Color position {i}")

    def draw_noise(self, layout, prop):
        layout.prop(prop, "name")
        layout.prop(prop, "scale")
        layout.prop(prop, "detail")
        layout.prop(prop, "roughness")
        layout.prop(prop, "distortion")
        layout.prop(prop, "mapping_scale")
        self.draw_colors(layout, prop)


    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Block 1: Create Material Section
        layout.label(text="Create a New Material:")
        layout.prop(scene, "texture_type")

        if scene.texture_type == 'TEX_IMAGE':
            self.draw_tex_image(layout, scene.image_properties)
        if scene.texture_type == 'NOISE':
            self.draw_noise(layout, scene.noise_properties)

        if scene.texture_type != 'NONE':
            layout.operator("material.apply_planar")