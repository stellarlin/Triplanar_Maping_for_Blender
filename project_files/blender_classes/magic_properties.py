import bpy
from .partial_properties import PartialProperties

class MagicProperties(PartialProperties):
    depth: bpy.props.IntProperty(
        name="Depth",
        description="Level of detail in turbulent noise",
        default=4,
        min=1,
        max=10,
    )

    distortion: bpy.props.FloatProperty(
        name="Distortion",
        description="Distortion of the noise texture",
        default=3,
        min=0.0,
        max=1.0,
    )

    def create_partial_inputs(self, group, texture_panel):
        group.interface.new_socket(
            name='Depth',
            in_out='INPUT',
            socket_type='NodeSocketInt',
            parent = texture_panel,
        )
        group.interface.items_tree['Depth'].default_value = self.depth
        group.interface.items_tree['Depth'].min_value = 1
        group.interface.items_tree['Depth'].max_value = 10

        group.interface.new_socket(
            name='Distortion',
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent=texture_panel
        )

        group.interface.items_tree['Distortion'].default_value = self.distortion
        group.interface.items_tree['Distortion'].min_value = -1000
        group.interface.items_tree['Distortion'].max_value = 1000

    def link_nodes(self, links, input_node, mapping_node, texture_node, bsdf_node, color_ramp):
        super().link_nodes(links, input_node, mapping_node, texture_node, bsdf_node, color_ramp)
        links.new(texture_node.outputs['Fac'], color_ramp.inputs['Fac'])
        links.new (input_node.outputs['Distortion'], texture_node.inputs['Distortion'])

    def create_texture(self, nodes, material):
        magic_node = nodes.new(type='ShaderNodeTexMagic')
        # Create a driver for the procedural_blend property

        driver = magic_node.driver_add('turbulence_depth').driver

        # Set up the driver type and target
        driver.type = 'SUM'
        var = driver.variables.new()
        var.name = "depth"  # Name of the driver variable
        var.type = 'SINGLE_PROP'

        # Target the Value node's output (node output or specific property)
        var.targets[0].id_type = 'MATERIAL'
        var.targets[0].id = material  # The Value node is the driver source
        var.targets[0].data_path = "node_tree.nodes[\"Group\"].inputs[\"Depth\"].default_value"

        return magic_node

    def reset(self):
        super().reset()
        self.depth = 4
        self.distortion = 3.0
