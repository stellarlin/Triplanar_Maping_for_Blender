import os
import bpy

class PlanarMapping_Properties(bpy.types.PropertyGroup):
    texture: bpy.props.StringProperty(
        name = "Texture",
        description = "Texture for x label",
        subtype = 'FILE_PATH')

    scale: bpy.props.FloatVectorProperty(
        name="Scale",
        description="Scale along X, Y, Z axes",
        default=(0.2, 0.2, 0.2),  # Default scale
        min=0.0,  # Minimum allowed value
        max=3.0,  # Maximum allowed value
        size=3,  # Number of components (X, Y, Z)
        subtype='XYZ'  # Display subtype for UI
    )

    blending: bpy.props.FloatProperty(
        name="Blending",
        description="",
        default=0.2)

    name: bpy.props.StringProperty(
        name="Texture Name",
        description="Name for the created material",
        default="DefaultPlanar_Material")  # Default name if no name is provided



    def create_triplanar_material(self, mathutils=None):

        # Create a new material
        material = bpy.data.materials.new(self.name)
        material.use_nodes = True

        # Access the material's node tree
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        nodes.clear()

        # Add the necessary nodes

        # TextureCoordinate
        texture_coord_node = nodes.new(type='ShaderNodeTexCoord')
        texture_coord_node.location = (0, 0)

        # Mapping
        mapping_node = nodes.new(type='ShaderNodeMapping')
        mapping_node.location = (200, 0)

        #mapping_node.inputs['Scale'].default_value  = self.scale
        mapping_node.inputs['Scale'].default_value[0] = self.scale[0]
        mapping_node.inputs['Scale'].default_value[1] = self.scale[1]
        mapping_node.inputs['Scale'].default_value[2] = self.blending

        texture_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')

        # Add a Diffuse BSDF shader
        diffuse_node = nodes.new(type='ShaderNodeBsdfDiffuse')
        # Add a Material Output node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')

        if os.path.isfile(bpy.path.abspath(self.texture)):
            try:
                texture_node.image = bpy.data.images.load(bpy.path.abspath(self.texture))
                print(f"Loaded texture from {texture_node}")

            except Exception as e:
                print(f"Failed to load texture {self.texture}: {e}. Using default white texture.")

        else:
            print(f"Warning: Texture file not found at {self.texture}.Using default texture")

        texture_node.projection = 'BOX'     # Set the projection type to 'BOX'
        texture_node.location = (200, 600)

        texture_node.inputs['Blending'] = self.blending
        texture_node.interpolation = 'Linear'

        # Connect the Texture Coordinate node to the Mapping node
        links.new(texture_coord_node.outputs['Generated'], mapping_node.inputs['Vector'])

        # Connect the Mapping node to the Texture node
        links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])

        # Connect the combined RGB to the diffuse shader
        links.new(texture_node.outputs['Color'], diffuse_node.inputs['Base Color'])

        # Connect the diffuse shader to the material output
        links.new(diffuse_node.outputs['BSDF'], output_node.inputs['Surface'])

        print(f"Material '{self.name}' created successfully.")
        return material

