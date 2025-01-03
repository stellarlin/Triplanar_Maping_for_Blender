import bpy


def choose_properties(context):
    if context.scene.texture_type == 'TEX_IMAGE':
        return context.scene.image_properties
    if context.scene.texture_type == 'NOISE':
        return context.scene.noise_properties
    if context.scene.texture_type == 'VORONOI':
        return context.scene.voronoi_properties
    if context.scene.texture_type == 'WAVES':
        return context.scene.wave_properties
    if context.scene.texture_type == 'MAGIC':
        return context.scene.magic_properties


class ApplyMaterialOperator(bpy.types.Operator):
    bl_idname = "material.apply_planar"
    bl_label = "Apply"
    bl_description = "Create a new material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = choose_properties(context)

        # Get the selected object
        if not context.selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}

        base_material = props.create_material()
        first_obj = True  # Flag to track if it's the first object
        for obj in context.selected_objects:

            if obj is None or obj.type != 'MESH':
                self.report({'WARNING'}, "Active object is not a mesh")
                continue

            if first_obj:
                # First object gets the base material directly
                obj.data.materials.clear()
                obj.data.materials.append(base_material)
                first_obj = False

            else:
                # For subsequent objects, create a copy of the base material
                new_material = base_material.copy()
                obj.data.materials.clear()
                obj.data.materials.append(new_material)

        self.report({'INFO'}, f"Applied {base_material.name} successfully")

        return {"FINISHED"}

class ResetPropertiesOperator(bpy.types.Operator):
    """Reset Partial Properties to Default"""
    bl_idname = "properties.reset_to_defaults"
    bl_label = "Reset the default properties"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Access the properties
        props = choose_properties(context)

        # Check if the properties object exists
        if not props:
            self.report({'ERROR'}, "Properties not found!")
            return {'CANCELLED'}

        # Call the method to reset properties to defaults
        props.reset()

        self.report({'INFO'}, "Properties reset to default values.")
        return {'FINISHED'}
