import bpy
from .partial_properties import PartialProperties

class NoiseProperties(PartialProperties):
    detail: bpy.props.FloatProperty(
        name="Detail",
        description="Detail of the noise texture",
        default=0,
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
        default=0.5,
        min=0.0,
        max=1.0,
    )

    def create_partial_inputs(self, group, texture_panel):
        group.interface.new_socket(
            name=self.detail.name,
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent = texture_panel,
        )
        group.interface.items_tree['Detail'].default_value = self.detail
        group.interface.items_tree['Detail'].min_value = self.detail.min
        group.interface.items_tree['Detail'].max_value = self.detail.max

        group.interface.new_socket(
            name= self.roughness.name,
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent=texture_panel,
        )

        group.interface.items_tree['Roughness'].default_value = self.roughness
        group.interface.items_tree['Roughness'].min_value = self.roughness.min
        group.interface.items_tree['Roughness'].max_value = self.roughness.max
        group.interface.items_tree['Roughness'].subtype = 'FACTOR'

        group.interface.new_socket(
            name=self.distortion.name,
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent=texture_panel
        )

        group.interface.items_tree['Distortion'].default_value = self.distortion
        group.interface.items_tree['Distortion'].min_value = self.distortion.min
        group.interface.items_tree['Distortion'].max_value = self.distortion.max
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