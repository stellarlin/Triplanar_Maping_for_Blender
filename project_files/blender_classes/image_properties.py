from .triplanar_properties import TriplanarMappingProperties
import bpy
import os

class ImageProperties(TriplanarMappingProperties):

    image_file: bpy.props.StringProperty(
        name = "File",
        description = "Texture for x label",
        subtype = 'FILE_PATH')

    blending: bpy.props.FloatProperty(
        name="Blending",
        description="",
        default=0.2
        )

    def create_inputs(self, group, texture_panel):
        super().create_inputs(group, texture_panel)
        group.interface.new_socket(
            name='Blending',
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent = texture_panel
        )

        group.interface.items_tree['Blending'].min_value = 0.0
        group.interface.items_tree['Blending'].max_value = 1.0
        group.interface.items_tree['Blending'].subtype = 'FACTOR'
        group.interface.items_tree['Blending'].default_value = self.blending

    def link_nodes(self, links, input_node, mapping_node, texture_node, bsdf_node, color_ramp):
        super().link_nodes(links, input_node, mapping_node, texture_node, bsdf_node, color_ramp)
        links.new(texture_node.outputs['Color'], bsdf_node.inputs['Base Color'])

    def create_texture(self, nodes, material):
        texture_node = nodes.new(type='ShaderNodeTexImage')
        if os.path.isfile(bpy.path.abspath(self.image_file)):
            try:
                texture_node.image = bpy.data.images.load(bpy.path.abspath(self.image_file))
                print(f"Loaded texture from {texture_node}")

            except Exception as e:
                print(f"Failed to load texture {self.image_file}: {e}. Using default white texture.")

        else:
            print(f"Warning: Texture file not found at {self.image_file}.Using default texture")

        texture_node.projection = 'BOX'  # Set the projection type to 'BOX'
        texture_node.projection_blend = self.blending
        texture_node.interpolation = 'Linear'

        # Create a driver for the procedural_blend property

        driver = texture_node.driver_add('projection_blend').driver

        # Set up the driver type and target
        driver.type = 'SUM'
        var = driver.variables.new()
        var.name = "blend"  # Name of the driver variable
        var.type = 'SINGLE_PROP'

        # Target the Value node's output (node output or specific property)
        var.targets[0].id_type = 'MATERIAL'
        var.targets[0].id = material  # The Value node is the driver source
        var.targets[0].data_path = "node_tree.nodes[\"Group\"].inputs[\"Blending\"].default_value"  # The value input/output property

        return texture_node

    def reset(self):
        super().reset()
        self.image_file = ""
        self.blending = 0.2