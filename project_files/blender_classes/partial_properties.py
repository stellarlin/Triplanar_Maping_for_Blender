from .triplanar_properties import TriplanarMappingProperties
import bpy
import os

class ColorPositionPair(bpy.types.PropertyGroup):
    color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0, 1.0),
        size=4,
        description="Color"
    )
    position: bpy.props.FloatProperty(
        name="Position",
        default=0.0,
        description="Position"
    )

class ColorPropertiesGroup(bpy.types.PropertyGroup):
    color_pair_1: bpy.props.PointerProperty(type=ColorPositionPair)
    color_pair_2: bpy.props.PointerProperty(type=ColorPositionPair)
    color_pair_3: bpy.props.PointerProperty(type=ColorPositionPair)
    color_pair_4: bpy.props.PointerProperty(type=ColorPositionPair)

    def create_color_input(self, group, number):
        group.interface.new_socket(
            name=f"Color {number}",
            in_out='INPUT',
            socket_type='NodeSocketColor'
        )

        group.interface.new_socket(
            name=f"Color position {number}",
            in_out='INPUT',
            socket_type='NodeSocketVector'
        )

        group.interface.items_tree[f"Color position {number}"].min_value = 0.0
        group.interface.items_tree[f"Color position {number}"].max_value = 1.0
        group.interface.items_tree[f"Color position {number}"].subtype = 'FACTOR'

        color_pair_attr = f"color_pair_{number}"
        if hasattr(self, color_pair_attr):
            color_pair = getattr(self, color_pair_attr)
            group.interface.items_tree[f"Color {number}"].default_value = color_pair.color
            group.interface.items_tree[f"Color position {number}"].default_value = color_pair.position

        else:
            group.interface.items_tree[f"Color {number}"].default_value = (1.0, 1.0, 1.0, 1.0)  # Default white if not set
            group.interface.items_tree[f"Color position {number}"].default_value = 0.0


    def create_inputs(self,group):
        group.interface.new_socket(
            name='Fac',
            in_out='INPUT',
            socket_type='NodeSocketFloat'
        )

        group.interface.items_tree['Fac'].min_value = 0.0
        group.interface.items_tree['Fac'].max_value = 1.0
        group.interface.items_tree['Fac'].subtype = 'FACTOR'

        for i in range(1, 5):
            self.create_color_input(group, i)

    def create_outputs(self, group):
        group.interface.new_socket(
            name=f"Color",
            in_out='INPUT',
            socket_type='NodeSocketColor'
        )

    def create_color_ramps(self, nodes):
        color_ramps = []
        y_offset = 200
        for i in range(3):
            color_ramp = nodes.new(type="ShaderNodeValToRGB")
            color_ramp.location = (200, 200 - i *200)
            color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)  # Black
            color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1)  # White
            color_ramps.append(color_ramp)
            y_offset -= 200
        return color_ramps

    def create_mixRGB (self, nodes):
        mix_nodes = []
        for i in range(3):
            mix_node = nodes.new(type="ShaderNodeMix")
            mix_node.blend_type = 'MIX'
            mix_node.data_type = 'RGBA'
            mix_node.clamp_factor = True
            mix_node.location = (400 + i * 200, 0)
            mix_nodes.append(mix_node)
        return mix_nodes

    def link_mix_color_ramp(self, color_ramps, mix_nodes, links):
        # Connect the color ramps and MixRGB nodes
        for i in range(3):
            links.new(color_ramps[i].outputs['Color'], mix_nodes[i].inputs['Factor'])
            if i + 1 < len(mix_nodes):  # Ensure we're within the valid range for the next MixRGB node
                links.new(mix_nodes[i].outputs['Result'], mix_nodes[i + 1].inputs['A'])  # Output of current Mix to next Mix

    def link_inputs(self, group, links, mix_nodes):
        for i in range(1, 5):
            if i == 1:
                links.new(group.interface.items_tree[f"Color {i}"], mix_nodes[i - 1].inputs['A'])
            else:
                links.new(group.interface.items_tree[f"Color {i}"], mix_nodes[i - 2].inputs['B'])


def create_custom_ramp(self, texture_node):
        node_group = bpy.data.node_groups.new("CustomColorRamp", "ShaderNodeTree")
        nodes = node_group.nodes
        links = node_group.links

        #create inputs
        self.create_inputs(node_group)
        input_node = node_group.nodes.new("NodeGroupInput")
        input_node.location = (-200,0)


        #create outputs
        self.reate_outputs(node_group)
        output_node = node_group.nodes.new("NodeGroupOutput")
        output_node.location = (800, 0)

        # Create four color ramp nodes
        color_ramps = self.create_color_ramps(nodes)
        mix_nodes = self.create_mixRGB(nodes)

        self.link_mix_color_ramp(color_ramps, mix_nodes, links)
        self.link_inputs(node_group, links, mix_nodes)

        links.new(mix_nodes[2].outputs['Result'], node_group.interface.items_tree["Color"])
        return node_group

class PartialProperties(TriplanarMappingProperties):

    scale: bpy.props.FloatVectorProperty(
        name ="Scale",
        description ="Scale of the texture",
        min = -1000,  # Minimum allowed value
        max = 1000,  # Maximum allowed value
    )
    colors: bpy.props.PointerProperty(type=ColorPropertiesGroup)

    def create_inputs(self, group):
        group.interface.new_socket(
            name='Texture Scale',
            in_out='INPUT',
            socket_type='NodeSocketFloat'
        )
        group.interface.items_tree['Texture Scale'].default_value = self.scale
        group.interface.items_tree['Texture Scale'].min_value = self.scale.min
        group.interface.items_tree['Texture Scale'].max_value = self.scale.max



    def link_inputs(self, links, input_node, mapping_node, texture_node):
        links.new(input_node.outputs['Mapping Scale'], mapping_node.inputs['Scale'])
        return

    def create_texture(self, nodes, material):

        return texture_node