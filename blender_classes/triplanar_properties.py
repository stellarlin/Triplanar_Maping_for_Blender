import os

import bpy


def create_texture_mix_node(material, separate_xyz_node, image_texture_node, axis, location):
    # Create a MixRGB node
    mix_rgb_node = material.node_tree.nodes.new(type='ShaderNodeMixRGB')
    mix_rgb_node.location = location

    # Connect the axis output from the SeparateXYZ node to the MixRGB node
    material.node_tree.links.new(separate_xyz_node.outputs[axis], mix_rgb_node.inputs[0])

    # Connect the image texture node to the MixRGB node
    material.node_tree.links.new(image_texture_node.outputs['Color'], mix_rgb_node.inputs[1])

    return mix_rgb_node


class TriplanarProperties(bpy.types.PropertyGroup):
    texture_x: bpy.props.StringProperty(
        name = "Texture X",
        description = "Texture for x label",
        subtype = 'FILE_PATH')

    texture_y: bpy.props.StringProperty(
        name="Texture Y",
        description="Texture for y label",
        subtype='FILE_PATH')

    texture_z: bpy.props.StringProperty(
        name="Texture Z",
        description="Texture for z label",
        subtype='FILE_PATH')
    
    scale: bpy.props.FloatProperty(
        name="Scale",
        description="",
        default=1.0)

    blending: bpy.props.FloatProperty(
        name="Scale",
        description="",
        default=0.2)

    name: bpy.props.StringProperty(
        name="Texture Name",
        description="Name for the created material",
        default="DefaultTriplanarMaterial")  # Default name if no name is provided




    def create_triplanar_material(self):

        # Create a new material
        material = bpy.data.materials.new(name=self.name)
        material.use_nodes = True
        # Access the material's node tree
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        nodes.clear()

        # Add the necessary nodes
        texture_coord_node = nodes.new(type='ShaderNodeTexCoord')
        texture_coord_node.location = (0, 0)

        mapping_node = nodes.new(type='ShaderNodeMapping')
        mapping_node.location = (200, 0)


        separate_xyz_node = nodes.new(type='ShaderNodeSeparateXYZ')
        separate_xyz_node.location = (400, 0)

        # Add a Diffuse BSDF shader
        diffuse_node = nodes.new(type='ShaderNodeBsdfDiffuse')
        # Add a Material Output node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')

        texture_node = self.create_texture(material, self.texture_x,(600, 200))
        # Set the projection type to 'BOX'
        texture_node.projection = 'BOX'
       # texture_nodes = [self.create_texture(material, self.texture_x,(600, 200)),
        #self.create_texture(material, self.texture_y, (600, 0)),
       # self.create_texture(material, self.texture_z, (600, -200))]

        # Connect the Texture Coordinate node to the Mapping node
        links.new(texture_coord_node.outputs['Generated'], mapping_node.inputs['Vector'])

        # Connect the Mapping node to the Texture node
        links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])

        # Connect the combined RGB to the diffuse shader
        links.new(texture_node.outputs['Color'], diffuse_node.inputs['Base Color'])

        # Connect the diffuse shader to the material output
        links.new(diffuse_node.outputs['BSDF'], output_node.inputs['Surface'])

        print(f"Material '{self.name}' created successfully.")
        return material

    def create_texture(self, material, texture_path, location):
        if not texture_path:
            print("No texture path provided.")
            return self.create_default_white_texture(location)

        if  os.path.isfile(bpy.path.abspath(texture_path)):
            # print(f"Warning: Texture file not found at {texture_path}.Using default texture")
            # Create a new image if no valid path is provided
            # return self.create_default_texture()
            image_node = material.node_tree.nodes.new(type='ShaderNodeTexImage')
            try:
                image_node.image = bpy.data.images.load(bpy.path.abspath(texture_path))
                image_node.location = location
                print(f"Loaded texture from {texture_path}")
            except Exception as e:
                print(f"Failed to load texture {texture_path}: {e}. Using default white texture.")
            return image_node
