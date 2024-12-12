import os
import bpy



class TriplanarMapping_Properties( bpy.types.PropertyGroup):


    name: bpy.props.StringProperty(
        name="Name",
        description="Name for the created material",
        default="DefaultPlanar_Material")  # Default name if no name is provided


    def create_texture(self, nodes):
        # This method should be implemented by subclasses.
        return nodes.new(type='ShaderNodeTexImage')


    def create_material(self):

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

        mapping_node.inputs['Scale'].default_value = self.scale

        # Add a Diffuse BSDF shader
        principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled_node.location = (800, 0)
        # Add a Material Output node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (1100, 0)

        texture_node = self.create_texture(nodes)

        # Connect the Texture Coordinate node to the Mapping node
        links.new(texture_coord_node.outputs['Generated'], mapping_node.inputs['Vector'])

        # Connect the Mapping node to the Texture node
        links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])

        # Connect the combined RGB to the diffuse shader
        links.new(texture_node.outputs['Color'], principled_node.inputs['Base Color'])

        # Connect the diffuse shader to the material output
        links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

        print(f"Material '{self.name}' created successfully.")
        return material


    def update_material(self, context):
        # Get the active material
        material = context.object.active_material

        if not material:
            print(f"No active material found.")
            return

        # Ensure the material has a node tree
        if not material.use_nodes or not material.node_tree:
            print(f"Material does not use nodes.")
            return

        material.name = self.name


class TextureImage_Properties(TriplanarMapping_Properties):

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
        default=0.2
        )

    def create_texture(self, nodes):
        texture_node = nodes.new(type='ShaderNodeTexImage')
        if os.path.isfile(bpy.path.abspath(self.texture)):
            try:
                texture_node.image = bpy.data.images.load(bpy.path.abspath(self.texture))
                print(f"Loaded texture from {texture_node}")

            except Exception as e:
                print(f"Failed to load texture {self.texture}: {e}. Using default white texture.")

        else:
            print(f"Warning: Texture file not found at {self.texture}.Using default texture")

        texture_node.projection = 'BOX'  # Set the projection type to 'BOX'
        texture_node.projection_blend = self.blending
        texture_node.interpolation = 'Linear'
        texture_node.location = (400, 0)

        return texture_node

    def update_material(self, context):

        super().update_material(context)

        # Get the active material
        material = context.object.active_material

        if not material:
            print(f"No active material found.")
            return

        # Ensure the material has a node tree
        if not material.use_nodes or not material.node_tree:
            print(f"Material does not use nodes.")
            return

        # Find the Image Texture node
        nodes = material.node_tree.nodes
        texture_node = None
        mapping_node = None

        for node in nodes:
            if texture_node and mapping_node:
                break
            if node.type == 'TEX_IMAGE':  # Look for Image Texture nodes
                texture_node = node
            if node.type == 'MAPPING':
                mapping_node = node

        if not texture_node or not mapping_node:
            print(f"No Image Texture or Mapping Node found.")
            return

        # Modify the Blend property
        texture_node.projection_blend = self.blending
        mapping_node.inputs['Scale'].default_value = self.scale
