import bpy





class ApplyMaterialOperator(bpy.types.Operator):
    bl_idname = "material.apply_planar"
    bl_label = "Apply"
    bl_description = "Create a new material"
    bl_options = {'REGISTER', 'UNDO'}

    def choose_properties(self, context):
        if context.scene.texture_type == 'TEX_IMAGE':
            return context.scene.image_properties
        if context.scene.texture_type == 'NOISE':
            return context.scene.noise_properties

    def execute(self, context):
        props = self.choose_properties(context)

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
