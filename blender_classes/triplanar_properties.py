
import bpy

class TriplanarMapping_Properties( bpy.types.PropertyGroup):


    name: bpy.props.StringProperty(
        name="Name",
        description="Name for the created material",
        default="DefaultPlanar_Material")  # Default name if no name is provided


    def create_texture(self, nodes):
        # This method should be implemented by subclasses.
        return nodes.new(type='ShaderNodeTexImage')


    def create_material(self):

        # Create a new material
        material = bpy.data.materials.new(self.name)
        material.use_nodes = True

        # Access the material's node tree
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        nodes.clear()

        # Add the necessary nodes

        # TextureCoordinate
        texture_coord_node = nodes.new(type='ShaderNodeTexCoord')
        texture_coord_node.location = (0, 0)

        # Mapping
        mapping_node = nodes.new(type='ShaderNodeMapping')
        mapping_node.location = (200, 0)

        mapping_node.inputs['Scale'].default_value = self.scale

        # Add a Diffuse BSDF shader
        principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        principled_node.location = (800, 0)
        # Add a Material Output node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (1100, 0)

        texture_node = self.create_texture(nodes)

        # Connect the Texture Coordinate node to the Mapping node
        links.new(texture_coord_node.outputs['Generated'], mapping_node.inputs['Vector'])

        # Connect the Mapping node to the Texture node
        links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])

        # Connect the combined RGB to the diffuse shader
        links.new(texture_node.outputs['Color'], principled_node.inputs['Base Color'])

        # Connect the diffuse shader to the material output
        links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

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

