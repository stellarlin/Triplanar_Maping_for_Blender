import bpy
from .partial_properties import PartialProperties

class NoiseProperties(PartialProperties):
    detail: bpy.props.FloatProperty(
        name="Detail",
        description="Detail of the noise texture",
        default=5,
        min=-1000,
        max=1000,
    )
    roughness: bpy.props.FloatProperty(
        name="Roughness",
        description="Roughness of the noise texture",
        default=0.5,
        min=0.0,
        max=1.0,
    )

    distortion: bpy.props.FloatProperty(
        name="Distortion",
        description="Distortion of the noise texture",
        default=0,
        min=0.0,
        max=1.0,
    )

    def create_partial_inputs(self, group, texture_panel):
        group.interface.new_socket(
            name='Detail',
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent = texture_panel,
        )
        group.interface.items_tree['Detail'].default_value = self.detail
        group.interface.items_tree['Detail'].min_value = -1000
        group.interface.items_tree['Detail'].max_value = 1000

        group.interface.new_socket(
            name= 'Roughness',
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent=texture_panel,
        )

        group.interface.items_tree['Roughness'].default_value = self.roughness
        group.interface.items_tree['Roughness'].min_value = 0.0
        group.interface.items_tree['Roughness'].max_value = 1.0
        group.interface.items_tree['Roughness'].subtype = 'FACTOR'

        group.interface.new_socket(
            name='Distortion',
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent=texture_panel
        )

        group.interface.items_tree['Distortion'].default_value = self.distortion
        group.interface.items_tree['Distortion'].min_value = 0.0
        group.interface.items_tree['Distortion'].max_value = 0.1
        group.interface.items_tree['Distortion'].subtype = 'FACTOR'

    def link_inputs(self, links, input_node, mapping_node, texture_node, color_ramp):
        super().link_inputs(links, input_node, mapping_node, texture_node, color_ramp)
        links.new (input_node.outputs['Detail'], texture_node.inputs['Detail'])
        links.new (input_node.outputs['Roughness'], texture_node.inputs['Roughness'])
        links.new (input_node.outputs['Distortion'], texture_node.inputs['Distortion'])

    def create_texture(self, nodes, material):
        noise_texture_node = nodes.new(type='ShaderNodeTexNoise')
        noise_texture_node.noise_dimensions = '3D'
        noise_texture_node.normalize = True
        noise_texture_node.noise_type='FBM'

        return noise_texture_node

    def reset(self):
        super().reset()
        self.detail = 5
        self.roughness = 0.5
        self.distortion = 0
