import bpy


class Apply_Material_Operator(bpy.types.Operator):
    bl_idname = "material.apply_planar"
    bl_label = "Apply Material"
    bl_description = "Create a new material"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        if context.scene.texture_type == 'TEX_IMAGE':
            props = context.scene.image_properties
      #  elif context.scene.texture_type == 'NOISE':
      #      props = context.scene.noise_properties

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

class Update_Material_Operator(bpy.types.Operator):
    bl_idname = "material.update_planar"
    bl_label = "Update Material"
    bl_description = "Update a material of selected mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.scene.texture_type == 'TEX_IMAGE':
            props = context.scene.image_properties
     #   elif context.scene.texture_type == 'NOISE':
     #       props = context.scene.noise_properties

        props.update_material(context)  # Trigger the update method
        return {'FINISHED'}
