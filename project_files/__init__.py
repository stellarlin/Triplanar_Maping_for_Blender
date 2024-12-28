# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


bl_info = {
    "name": "Triplane Texture Mapping",
    "author": "Sofiia Prykhach",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Tool Shelf",
    "description": "",
    "warning": "",
    "doc_url": "",
    "category": "",
}

from .blender_classes import triplanar_properties as properties
from .blender_classes import triplanar_operator as operator
from .blender_classes import triplanar_panel as panel
from .blender_classes.image_properties import ImageProperties
from .blender_classes.partial_properties import  PartialProperties
from .blender_classes.partial_properties import  ColorPositionPair
from .blender_classes.noise_properties import  NoiseProperties
from .blender_classes.voronoi_properties import  VoronoiProperties


import bpy

#auto_load.init()

# List of classes to register
classes = [
    properties.TriplanarMappingProperties,
    operator.ApplyMaterialOperator,
    panel.PlanarMappingPanel,
]


def register():
    # Register each class in the list
    #for cls in classes:
    #    bpy.utils.register_class(cls)

    bpy.utils.register_class(properties.TriplanarMappingProperties)
    bpy.utils.register_class(ImageProperties)
    bpy.utils.register_class(ColorPositionPair)
    bpy.utils.register_class(PartialProperties)
    bpy.utils.register_class(NoiseProperties)
    bpy.utils.register_class(VoronoiProperties)

    bpy.utils.register_class(operator.ApplyMaterialOperator)
    bpy.utils.register_class(operator.ResetMaterialPropertiesOperator)
    bpy.utils.register_class(panel.PlanarMappingPanel)

    bpy.types.Scene.texture_type = bpy.props.EnumProperty(
        name="Type",
        description="Choose a type",
        items=[
            ('NONE', "-", "No type selected"),
            ('TEX_IMAGE', "Image", "Properties for Texture Image"),
            ('NOISE', "Noise", "Properties for Noise"),
            ('VORONOI', "Voronoi", "Properies for Voronoi Texture"),
        ],
        default='NONE'
    )
    bpy.types.Scene.image_properties = bpy.props.PointerProperty(type=ImageProperties)
    bpy.types.Scene.noise_properties = bpy.props.PointerProperty(type=NoiseProperties)
    bpy.types.Scene.voronoi_properties = bpy.props.PointerProperty(type=VoronoiProperties)

def unregister():
    # Unregister each class in the list
   # for cls in reversed(classes):
   #     bpy.utils.unregister_class(cls)

    bpy.utils.unregister_class(properties.TriplanarMappingProperties)
    bpy.utils.unregister_class(ImageProperties)
    bpy.utils.unregister_class(ColorPositionPair)
    bpy.utils.unregister_class(PartialProperties)
    bpy.utils.uregister_class(NoiseProperties)
    bpy.utils.unregister_class(VoronoiProperties)

    bpy.utils.unregister_class(operator.ApplyMaterialOperator)
    bpy.utils.unregister_class(operator.ResetMaterialPropertiesOperator)
    bpy.utils.unregister_class(panel.PlanarMappingPanel)

    # Unregister properties if needed
    del bpy.types.Scene.image_properties
    del bpy.types.Scene.noise_properties
    del bpy.types.Scene.voronoi_properties

if __name__ == "__main__":
    register()