import bpy
from .partial_properties import PartialProperties

class VoronoiProperties(PartialProperties):
    detail: bpy.props.FloatProperty(
        name="Detail",
        description="Detail of the voronoi texture",
        default=5,
        min=-1000,
        max=1000,
    )
    roughness: bpy.props.FloatProperty(
        name="Roughness",
        description="Roughness of the voronoi texture",
        default=0.5,
        min=0.0,
        max=1.0,
    )

    randomness: bpy.props.FloatProperty(
        name="Randomness",
        description="Randomness of the voronoi texture",
        default=0.5,
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
            name='Randomness',
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent=texture_panel
        )

        group.interface.items_tree['Randomness'].default_value = self.randomness
        group.interface.items_tree['Randomness'].min_value = 0.0
        group.interface.items_tree['Randomness'].max_value = 0.1
        group.interface.items_tree['Randomness'].subtype = 'FACTOR'

    def link_nodes(self, links, input_node, mapping_node, texture_node, bsdf_node, color_ramp):
        super().link_nodes(links, input_node, mapping_node, texture_node, bsdf_node, color_ramp)
        links.new(texture_node.outputs['Color'], color_ramp.inputs['Fac'])

        links.new (input_node.outputs['Detail'], texture_node.inputs['Detail'])
        links.new (input_node.outputs['Roughness'], texture_node.inputs['Roughness'])
        links.new (input_node.outputs['Randomness'], texture_node.inputs['Randomness'])


    def create_texture(self, nodes, material):
        voronoi_node= nodes.new(type="ShaderNodeTexVoronoi")
        voronoi_node.feature = 'F1'
        voronoi_node.distance = 'MANHATTAN'
        voronoi_node.voronoi_dimensions = '3D'
        voronoi_node.normalize = True

        return voronoi_node

    def reset(self):
        super().reset()
        self.detail = 5
        self.roughness = 0.5
        self.randomness = 0.5