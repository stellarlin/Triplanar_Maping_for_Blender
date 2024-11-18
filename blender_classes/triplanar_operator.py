import bpy


class TriplanarOperator(bpy.types.Operator):
    bl_idname = "object.apply_triplanar_mapping"
    bl_label = "Apply Triplanar Mapping"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the selected object
        obj = context.active_object

        # Check if the selected object is a mesh
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Active object is not a mesh")
            return {'CANCELLED'}

        # Get the TriplanarProperties from the scene
        triplanar_props = context.scene.triplanar_properties

        # Create the triplanar material using the properties
        material = triplanar_props.create_triplanar_material()

        if material:
            # Apply the created material to the selected object
            if obj.data.materials:
                obj.data.materials[0] = material  # Replace first material
            else:
                obj.data.materials.append(material)  # Add material if no existing materials

            self.report({'INFO'}, f"Applied triplanar material: {material.name}")
            return {'FINISHED'}

        self.report({'ERROR'}, "Failed to create triplanar material.")
        return {'CANCELLED'}
