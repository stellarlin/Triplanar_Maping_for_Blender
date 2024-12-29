from distutils.core import setup_keywords

import bpy
from .partial_properties import PartialProperties

class WaveProperties(PartialProperties):
    wave_type: bpy.props.EnumProperty(
        name="Wave Type",
        description="Type of wave pattern",
        items=[
            ('BANDS', "Bands", "Generate bands as the wave pattern"),
            ('RINGS', "Rings", "Generate concentric rings as the wave pattern"),
        ],
        default='BANDS'
    )

    bands_direction: bpy.props.EnumProperty(
        name="Wave Direction",
        description="Direction of the wave bands",
        items=[
            ('X', "X", "Wave bands aligned along the X axis"),
            ('Y', "Y", "Wave bands aligned along the Y axis"),
            ('Z', "Z", "Wave bands aligned along the Z axis"),
            ('DIAGONAL', "Diagonal", "Wave bands aligned diagonally"),
        ],
        default='X'
    )

    rings_direction: bpy.props.EnumProperty(
        name="Wave Direction",
        description="Direction of the wave bands",
        items=[
            ('X', "X", "Wave bands aligned along the X axis"),
            ('Y', "Y", "Wave bands aligned along the Y axis"),
            ('Z', "Z", "Wave bands aligned along the Z axis"),
            ('SPHERICAL', "Spherical", "Wave bands aligned spherically"),
        ],
        default='X'
    )

    wave_profile: bpy.props.EnumProperty(
        name="Wave Profile",
        description="Choose the wave profile",
        items=[
            ('SIN', "Sine", "Default sine wave"),
            ('SAW', "Saw", "Sawtooth wave"),
            ('TRI', "Triangle", "Triangle wave"),
        ],
        default='SIN'
    )


    distortion: bpy.props.FloatProperty(
        name="Distortion",
        description="Distortion of the noise texture",
        default=5.5,
        min=-1000,
        max=1000,
    )

    detail: bpy.props.FloatProperty(
        name="Detail",
        description="Detail of the noise texture",
        default=5,
        min=-1000,
        max=1000,
    )

    detail_scale: bpy.props.FloatProperty(
        name="Detail Scale",
        description="",
        default=0.5,
        min=-1000,
        max=1000,
    )

    detail_roughness: bpy.props.FloatProperty(
        name="Detail Roughness",
        description="",
        default=0.5,
        min=0.0,
        max=1.0,
    )


    def create_partial_inputs(self, group, texture_panel):
        # add an inputs for drivers

        group.interface.new_socket(
            name='Distortion',
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent=texture_panel
        )

        group.interface.items_tree['Distortion'].default_value = self.distortion
        group.interface.items_tree['Distortion'].min_value = -1000
        group.interface.items_tree['Distortion'].max_value = 1000

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
            name='Detail Scale',
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent=texture_panel,
        )
        group.interface.items_tree['Detail Scale'].default_value = self.detail_scale
        group.interface.items_tree['Detail Scale'].min_value = -1000
        group.interface.items_tree['Detail'].max_value = 1000

        group.interface.new_socket(
            name= 'Detail Roughness',
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent=texture_panel,
        )

        group.interface.items_tree['Detail Roughness'].default_value = self.detail_roughness
        group.interface.items_tree['Detail Roughness'].min_value = 0.0
        group.interface.items_tree['Detail Roughness'].max_value = 1.0
        group.interface.items_tree['Detail Roughness'].subtype = 'FACTOR'



    def link_inputs(self, links, input_node, mapping_node, texture_node, color_ramp):
        super().link_inputs(links, input_node, mapping_node, texture_node, color_ramp)
       # todo wave set inputs
        links.new (input_node.outputs['Detail'], texture_node.inputs['Detail'])
        links.new(input_node.outputs['Detail Scale'], texture_node.inputs['Detail Scale'])
        links.new (input_node.outputs['Detail Roughness'], texture_node.inputs['Detail Roughness'])
        links.new (input_node.outputs['Distortion'], texture_node.inputs['Distortion'])

    def create_texture(self, nodes, material):
        wave_node = nodes.new(type='ShaderNodeTexWave')
        wave_node.wave_type = self.wave_type
        wave_node.wave_profile = self.wave_profile
        if wave_node.wave_type == 'BANDS':
            wave_node.bands_direction = self.bands_direction
        else:
            wave_node.rings_direction = self.rings_direction

        return wave_node

    def reset(self):
        super().reset()
        self.wave_type = 'BANDS'
        self.wave_profile = 'SIN'
        self.bands_direction = 'X'
        self.rings_direction = 'X'

        self.distortion = 5.5
        self.detail = 5
        self.detail_scale = 0.5
        self.detail_roughness = 0.5
