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

    def create_inputs(self, nodes):
        inputs = nodes.new('NodeGroupInput')
        inputs.location = (-350, 0)

        mapping_scale_input = inputs.new("NodeSocketVector", "Mapping Scale")
        mapping_scale_input.default_value = self.scale

        blend_input = inputs.new("NodeSocketFloat", "Texture Blend")
        blend_input.default_value = self.blending

        return inputs

    def create_outputs(self, nodes):
        outputs = nodes.new('NodeGroupOutput')
        outputs.location = (1100, 0)
        outputs.new("NodeSocketShader", "BSDF")
        return outputs

    def link_inputs(self, inputs, links, mapping_node, texture_node):
        links.new(inputs['Scale'], mapping_node.inputs['Scale'])
        return

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

        # Add a driver to the 'Blend' property
        driver = texture_node.inputs["Blend"].driver_add("default_value").driver
        driver.type = 'SUM'

        # Add a variable to the driver
        var = driver.variables.new()
        var.name = "group_input"
        var.type = 'SINGLE_PROP'

        # Set the target for the variable
        target = var.targets[0]
        target.id = material  # Reference the material
        target.data_path = 'node_tree.nodes["Group"].inputs["Blend"].default_value'

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
