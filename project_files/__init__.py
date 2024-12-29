
bl_info = {
    "name": "Triplanar Texture Mapping",
    "author": "Sofiia Prykhach",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "Properties > Material Tab > Triplanar Mapping",
    "description": "Adds triplanar texture mapping functionality to Blender, enabling seamless texturing without UV maps.",
    "warning": "",
    "doc_url": "",
    "category": "Material",
}

from .blender_classes import triplanar_properties as properties
from .blender_classes import triplanar_operator as operator
from .blender_classes import triplanar_panel as panel
from .blender_classes.image_properties import ImageProperties
from .blender_classes.partial_properties import  PartialProperties
from .blender_classes.partial_properties import  ColorPositionPair
from .blender_classes.noise_properties import  NoiseProperties
from .blender_classes.voronoi_properties import  VoronoiProperties
from .blender_classes.wave_properties import  WaveProperties
from .blender_classes.magic_properties import  MagicProperties

import bpy

#auto_load.init()

# List of classes to register
classes = [
    properties.TriplanarMappingProperties,
    operator.ApplyMaterialOperator,
    panel.TriplanarMappingPanel,
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
    bpy.utils.register_class(MagicProperties)
    bpy.utils.register_class(WaveProperties)


    bpy.utils.register_class(operator.ApplyMaterialOperator)
    bpy.utils.register_class(operator.ResetPropertiesOperator)
    bpy.utils.register_class(panel.TriplanarMappingPanel)

    bpy.types.Scene.texture_type = bpy.props.EnumProperty(
        name="Type",
        description="Choose a type",
        items=[
            ('NONE', "-", "No type selected"),
            ('TEX_IMAGE', "Image", "Properties for Texture Image"),
            ('NOISE', "Noise", "Properties for Noise"),
            ('VORONOI', "Voronoi", "Properies for Voronoi Texture"),
            ('WAVES', "Waves", "Properies for Wave Texture"),
            ('MAGIC', "Magic", "Properies for Magic Texture"),
        ],
        default='NONE'
    )
    bpy.types.Scene.image_properties = bpy.props.PointerProperty(type=ImageProperties)
    bpy.types.Scene.noise_properties = bpy.props.PointerProperty(type=NoiseProperties)
    bpy.types.Scene.voronoi_properties = bpy.props.PointerProperty(type=VoronoiProperties)
    bpy.types.Scene.wave_properties = bpy.props.PointerProperty(type=WaveProperties)
    bpy.types.Scene.magic_properties = bpy.props.PointerProperty(type=MagicProperties)


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
    bpy.utils.unregister_class(MagicProperties)
    bpy.utils.unregister_class(WaveProperties)


    bpy.utils.unregister_class(operator.ApplyMaterialOperator)
    bpy.utils.unregister_class(operator.ResetPropertiesOperator)
    bpy.utils.unregister_class(panel.TriplanarMappingPanel)

    # Unregister properties if needed
    del bpy.types.Scene.image_properties
    del bpy.types.Scene.noise_properties
    del bpy.types.Scene.voronoi_properties
    del bpy.types.Scene.wave_properties
    del bpy.types.Scene.magic_properties

if __name__ == "__main__":
    register()