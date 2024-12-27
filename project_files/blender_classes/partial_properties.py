from .triplanar_properties import TriplanarMappingProperties
import bpy

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


class PartialProperties(TriplanarMappingProperties):

    scale: bpy.props.FloatProperty(
        name ="Scale",
        description ="Scale of the texture",
        min = -1000,  # Minimum allowed value
        max = 1000,  # Maximum allowed value
        default = 30
    )

    color_pair_1: bpy.props.PointerProperty(type=ColorPositionPair)
    color_pair_2: bpy.props.PointerProperty(type=ColorPositionPair)
    color_pair_3: bpy.props.PointerProperty(type=ColorPositionPair)
    color_pair_4: bpy.props.PointerProperty(type=ColorPositionPair)

    def partial(self):
        return True

    def init_default_colors(self):
        """Set the default values for color pairs."""
        self.color_pair_1.color = (0.0, 0.0, 0.0, 1.0)  # #000000FF - black
        self.color_pair_1.position = 0.125

        self.color_pair_2.color = (0.3, 0.3, 0.3, 1.0)  # #4D4D4DFF - dark grey
        self.color_pair_2.position = 0.250

        self.color_pair_3.color = (0.58, 0.58, 0.58, 1.0)  # #949494FF - light grey
        self.color_pair_3.position = 0.5
        self.color_pair_4.color = (1.0, 1.0, 1.0, 1.0)  # #FFFFFFFF - white
        self.color_pair_4.position = 1


    def create_color_input(self, group, number, panel):
        group.interface.new_socket(
            name=f"Color {number}",
            in_out='INPUT',
            socket_type='NodeSocketColor',
            parent = panel
        )

    def create_position_input(self, group, number, panel):
        group.interface.new_socket(
            name=f"Color position {number}",
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent = panel
        )

        group.interface.items_tree[f"Color position {number}"].min_value = 0.0
        group.interface.items_tree[f"Color position {number}"].max_value = 1.0
        group.interface.items_tree[f"Color position {number}"].subtype = 'FACTOR'

    def set_color_pair_input (self, group, number):
        color_pair_attr = f"color_pair_{number}"
        if hasattr(self, color_pair_attr):
            color_pair = getattr(self, color_pair_attr)
            group.interface.items_tree[f"Color {number}"].default_value = color_pair.color
            group.interface.items_tree[f"Color position {number}"].default_value = color_pair.position

        else:
            group.interface.items_tree[f"Color {number}"].default_value = (
            1.0, 1.0, 1.0, 1.0)  # Default white if not set
            group.interface.items_tree[f"Color position {number}"].default_value = 0.0

    def create_partial_inputs(self, group, texture_panel):
        return

    def create_inputs(self, group, texture_panel):
        super().create_inputs(group, texture_panel)
        group.interface.new_socket(
            name='Scale',
            in_out='INPUT',
            socket_type='NodeSocketFloat',
            parent = texture_panel
        )
        group.interface.items_tree['Scale'].default_value = self.scale
        group.interface.items_tree['Scale'].min_value = -1000
        group.interface.items_tree['Scale'].max_value = 1000

        self.create_partial_inputs(group, texture_panel)

        panel = group.interface.new_panel(name = "Colors",
                                        description='Colors of the Color Ramp and their positions',
                                        default_closed=False)


        for i in range(1, 5):
            self.create_color_input(group, i, panel)
            self.create_position_input(group, i, panel)
            self.set_color_pair_input(group, i)

    def create_ramp_inputs(self, group):
        group.interface.new_socket(
            name='Fac',
            in_out='INPUT',
            socket_type='NodeSocketFloat'
        )

        group.interface.items_tree['Fac'].min_value = 0.0
        group.interface.items_tree['Fac'].max_value = 1.0
        group.interface.items_tree['Fac'].subtype = 'FACTOR'

        for i in range(1, 5):
            self.create_color_input(group, i, None)

    def create_ramp_outputs(self, group):
        group.interface.new_socket(
            name='Color',
            in_out='OUTPUT',
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

    def create_mix (self, nodes):
        mix_nodes = []
        for i in range(3):
            mix_node = nodes.new(type="ShaderNodeMix")
            mix_node.blend_type = 'MIX'
            mix_node.data_type = 'RGBA'
            mix_node.clamp_factor = True
            mix_node.location = (400 + i * 200, 0)
            mix_nodes.append(mix_node)
        return mix_nodes

    def create_ramp_drivers(self, color_ramps, material):
        for i in range(1, 5):
            if i == 4:
                pin = color_ramps[i - 2].color_ramp.elements[1]
            else:
                pin = color_ramps[i - 1].color_ramp.elements[0]


            # Create a driver for the pin's position
            driver = pin.driver_add("position").driver  # Add a driver for the 'position' property
            # Set up the driver type and target
            driver.type = 'SUM'
            var = driver.variables.new()
            var.name = "pos"  # Name of the driver variable
            var.type = 'SINGLE_PROP'

            # Target the Value node's output (node output or specific property)
            var.targets[0].id_type = 'MATERIAL'
            var.targets[0].id = material  # The Value node is the driver source
            var.targets[0].data_path = f"node_tree.nodes[\"Group\"].inputs[\"Color position {i}\"].default_value"  # The value input/output property

    def link_ramp(self, input_node, output_node, links, color_ramps, mix_nodes):
        # Connect the color ramps and MixRGB nodes
        for i in range(3):
            links.new(color_ramps[i].outputs['Color'], mix_nodes[i].inputs['Factor'])
            if i + 1 < len(mix_nodes):  # Ensure we're within the valid range for the next MixRGB node
                links.new(mix_nodes[i].outputs['Result'],
                          mix_nodes[i + 1].inputs['A'])  # Output of current Mix to next Mix

        # connect Fac to color ramps
        for i in range(3):
            links.new(input_node.outputs['Fac'], color_ramps[i].inputs['Fac'])

        for i in range(1, 5):
            if i == 1:
                links.new(input_node.outputs[f"Color {i}"], mix_nodes[i - 1].inputs['A'])
            else:
                links.new(input_node.outputs[f"Color {i}"], mix_nodes[i - 2].inputs['B'])

        # Connect Mix to OutputNode
        links.new(mix_nodes[2].outputs['Result'], output_node.inputs['Color'])

    def link_inputs(self, links, input_node, mapping_node, texture_node, color_ramp):
       #connect basic inputs
       super().link_inputs(links, input_node, mapping_node, texture_node, color_ramp)

       # connect scale
       links.new(input_node.outputs['Scale'], texture_node.inputs['Scale'])
       #connect Colors
       for i in range(1, 5):
            links.new(input_node.outputs[f"Color {i}"], color_ramp.inputs[f"Color {i}"])

    def create_ramp(self, material):
        node_group = bpy.data.node_groups.new(name="CustomRamp", type="ShaderNodeTree")
        nodes = node_group.nodes
        links = node_group.links

        # create inputs
        self.create_ramp_inputs(node_group)
        input_node = node_group.nodes.new("NodeGroupInput")
        input_node.location = (-200, 0)

        # create outputs
        self.create_ramp_outputs(node_group)
        output_node = node_group.nodes.new("NodeGroupOutput")
        output_node.location = (800, 0)

        # Create four color ramp nodes
        color_ramps = self.create_color_ramps(nodes)
        mix_nodes = self.create_mix(nodes)

        self.link_ramp(input_node, output_node, links, color_ramps, mix_nodes)
        self.create_ramp_drivers(color_ramps, material)
        return node_group