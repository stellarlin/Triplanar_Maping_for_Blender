import bpy


def choose_properties(context):
    props = context.scene.image_properties
    if context.scene.texture_type == 'TEX_IMAGE':
        return props
    if context.scene.texture_type == 'NOISE':
        props = context.scene.noise_properties
    props.init_default_colors()
    return props


class ApplyMaterialOperator(bpy.types.Operator):
    bl_idname = "material.apply_planar"
    bl_label = "Apply"
    bl_description = "Create a new material"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = choose_properties(context)

        # Get the selected object
        obj = context.active_object
        material = props.create_material()

        if not obj:
            self.report({'WARNING'}, "No active object selected")

        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Active object is not a mesh")
            return {'CANCELLED'}

        # Store the material in a property to reference it later
        # context.scene.created_material = material.name
        # self.report({'INFO'}, f"Material '{material.name}' created successfully")
        # Check if the selected object is a mesh

        if obj.data.materials:
            obj.data.materials[0] = material  # Apply to the first slot
        else:
            obj.data.materials.append(material)  # Add a new slot if none exists

        self.report({'INFO'}, f"Applied {material.name}")

        return {"FINISHED"}

class ResetMaterialPropertiesOperator(bpy.types.Operator):
    """Reset Partial Properties to Default"""
    bl_idname = "properties.reset_to_defaults"
    bl_label = "Reset to Default"
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
