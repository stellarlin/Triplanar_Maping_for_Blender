from .triplanar_properties import TriplanarMappingProperties
import bpy
import os

class ImageProperties(TriplanarMappingProperties):

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

    def create_inputs(self, group):
        group.interface.new_socket(
            name='Mapping Scale',
            in_out='INPUT',
            socket_type='NodeSocketVector'
        )
        group.interface.items_tree['Mapping Scale'].subtype = 'XYZ'
        group.interface.items_tree['Mapping Scale'].default_value = self.scale


        group.interface.new_socket(
            name='Texture Blend',
            in_out='INPUT',
            socket_type='NodeSocketFloat'
        )

        group.interface.items_tree['Texture Blend'].min_value = 0.0
        group.interface.items_tree['Texture Blend'].max_value = 1.0
        group.interface.items_tree['Texture Blend'].default_value = self.blending

        # def link_inputs(self, group, links, mapping_node, texture_node):
  #      links.new(group.inputs['Scale'], mapping_node.inputs['Scale'])
   #     return

    def create_texture(self, nodes, material):
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
