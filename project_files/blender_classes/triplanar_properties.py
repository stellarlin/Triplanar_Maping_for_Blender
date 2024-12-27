
import bpy

class TriplanarMappingProperties(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(
        name="Name",
        description="Name for the created material",
        default="DefaultPlanar_Material")  # Default name if no name is provided

    mapping_scale: bpy.props.FloatVectorProperty(
        name="Mapping Scale",
        description="Scale along X, Y, Z axes",
        default=(0.4, 0.4, 0.4),  # Default scale
        min=0.0,  # Minimum allowed value
        max=3.0,  # Maximum allowed value
        size=3,  # Number of components (X, Y, Z)
        subtype='XYZ'  # Display subtype for UI
    )

    def create_texture(self, nodes, material):
        # This method should be implemented by subclasses.
        return nodes.new(type='ShaderNodeTexImage')

    def create_ramp(self, material):
        return bpy.data.node_groups.new(name="CustomRamp", type="ShaderNodeTree")


    def partial(self):
        return False

    def init_default_colors(self):
        return

    def create_inputs(self, group, texture_panel):
        group.interface.new_socket(
            name='Mapping Scale',
            in_out='INPUT',
            socket_type='NodeSocketVector'
        )
        group.interface.items_tree['Mapping Scale'].subtype = 'XYZ'
        group.interface.items_tree['Mapping Scale'].default_value = self.mapping_scale
        return

    def create_outputs(self, group):
        group.interface.new_socket(
            name='BSDF',
            in_out='OUTPUT',
            socket_type='NodeSocketShader'
    )

    def link_inputs(self, links, input_node, mapping_node, texture_node, color_ramp):
        links.new(input_node.outputs['Mapping Scale'], mapping_node.inputs['Scale'])

    def link_outputs(self, links, output_node,  bsdf_node):
        links.new(output_node.inputs['BSDF'], bsdf_node.outputs["BSDF"])
        return

    def create_group (self,  material):

        node_group = bpy.data.node_groups.new("TriplanarMapping", "ShaderNodeTree")
        nodes = node_group.nodes
        links = node_group.links

        # Add inputs
        texture_panel = node_group.interface.new_panel(name="Texture Properties",
                                          description='Colors of the Color Ramp and their positions',
                                          default_closed=False)

        self.create_inputs(node_group, texture_panel)
        input_node = nodes.new(type='NodeGroupInput')
        input_node.location = (-350, 0)


        # Add outputs
        self.create_outputs(node_group)
        output_node = nodes.new(type='NodeGroupOutput')
        output_node.location = (1100, 0)

        # Add the necessary node
        # TextureCoordinate
        texture_coord_node = nodes.new(type='ShaderNodeTexCoord')
        texture_coord_node.location = (0, 0)

        # Mapping
        mapping_node = nodes.new(type='ShaderNodeMapping')
        mapping_node.location = (200, 0)

        # Add a Diffuse BSDF shader
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (1000, 0)

        texture_node = self.create_texture(nodes, material)
        texture_node.location = (400, 0)

        if self.partial():
            custom_ramp = nodes.new('ShaderNodeGroup')
            custom_ramp.node_tree = self.create_ramp(material)
            custom_ramp.location = (800, 0)

            links.new(texture_node.outputs['Fac'], custom_ramp.inputs['Fac'])
            links.new(custom_ramp.outputs['Color'], bsdf_node.inputs['Base Color'])
            self.link_inputs(links, input_node, mapping_node, texture_node, custom_ramp)
        else:
            links.new(texture_node.outputs['Color'], bsdf_node.inputs['Base Color'])
            self.link_inputs(links, input_node, mapping_node, texture_node, None)


        # Connect the Texture Coordinate node to the Mapping node
        links.new(texture_coord_node.outputs['Generated'], mapping_node.inputs['Vector'])
        # Connect the Mapping node to the Texture node
        links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])
        # Connect the combined RGB to the diffuse shader


        self.link_outputs(links, output_node, bsdf_node)

        return node_group

    def create_material(self):

        # Create a new material
        material = bpy.data.materials.new(self.name)
        material.use_nodes = True

        # Access the material's node tree
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        nodes.clear()

        # Add a new node group
        node_group = nodes.new('ShaderNodeGroup')
        node_group.node_tree = self.create_group(material)

        node_group.location = (0, 0)

        # Add a Material Output node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (1400, 0)

        # Connect the diffuse shader to the material output
        links.new(node_group.outputs['BSDF'], output_node.inputs['Surface'])

        print(f"Material '{self.name}' created successfully.")
        return material


    def update_material(self, context):
        # Get the active material
        material = context.object.active_material

        if not material:
            print(f"No active material found.")
            return

        # Ensure the material has a node tree
        if not material.use_nodes or not material.node_tree:
            print(f"Material does not use nodes.")
            return

        material.name = self.name

