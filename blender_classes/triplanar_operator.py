import bpy


class PlanarMapping_Operator(bpy.types.Operator):
    bl_idname = "material.apply_planar"
    bl_label = "Create Material"
    bl_description = "Create a new material"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        props = context.scene.planar_properties
        # Get the selected object
        obj = context.active_object
        material = props.create_triplanar_material()

        if not obj:
            self.report({'WARNING'}, "No active object selected")

        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Active object is not a mesh")
            return {'CANCELLED'}

        # Store the material in a property to reference it later
        context.scene.created_material = material.name
        self.report({'INFO'}, f"Material '{material.name}' created successfully")
        # Check if the selected object is a mesh

        if obj.data.materials:
            obj.data.materials[0] = self.material  # Apply to the first slot
        else:
            obj.data.materials.append(self.material)  # Add a new slot if none exists

        self.report({'INFO'}, f"Applied {self.material.name}")

        return {"FINISHED"}
