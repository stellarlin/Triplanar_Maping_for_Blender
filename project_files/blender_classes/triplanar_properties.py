
import bpy

class TriplanarMappingProperties(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty(
        name="Name",
        description="Name for the created material",
        default="DefaultPlanar_Material")  # Default name if no name is provided


    def create_texture(self, nodes, material):
        # This method should be implemented by subclasses.
        return nodes.new(type='ShaderNodeTexImage')

    def create_inputs(self, nodes):
        return nodes.new('NodeGroupInput')

    def create_outputs(self, nodes):
        return nodes.new('NodeGroupOutput')

    def link_inputs(self, inputs, links, mapping_node, texture_node):
        return

    def link_outputs(self, outputs, links, bsdf_node):
        links.new(outputs['BSDF'], bsdf_node.inputs["Color"])
        return

    def create_group (self,  material):

        node_group = bpy.data.node_groups.new("TriplanarMapping", "ShaderNodeTree")
        nodes = node_group.nodes
        links = node_group.links

        # Add inputs
        inputs = self.create_inputs( nodes)

        # Add outputs
        outputs = self.create_outputs( nodes)

        # Add the necessary node
        # TextureCoordinate
        texture_coord_node = nodes.new(type='ShaderNodeTexCoord')
        texture_coord_node.location = (0, 0)

        # Mapping
        mapping_node = nodes.new(type='ShaderNodeMapping')
        mapping_node.location = (200, 0)

        # Add a Diffuse BSDF shader
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (800, 0)

       # texture_node = self.create_texture(nodes, material)

        # Connect the Texture Coordinate node to the Mapping node
        links.new(texture_coord_node.outputs['Generated'], mapping_node.inputs['Vector'])
        # Connect the Mapping node to the Texture node
   #     links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])
        # Connect the combined RGB to the diffuse shader
    #    links.new(texture_node.outputs['Color'], BSDF_node.inputs['Base Color'])

        self.link_outputs(outputs, links, bsdf_node)
     #   self.link_inputs(inputs, links, mapping_node, texture_node)
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
        node_group.node_tree = self.create_group(nodes)

        node_group.location = (0, 0)

        # Add a Material Output node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (800, 0)

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

