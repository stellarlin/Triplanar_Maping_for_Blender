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
import bpy

#auto_load.init()

# List of classes to register
classes = [
    properties.PlanarMapping_Properties,
    operator.PlanarMapping_Operator,
    panel.PlanarMapping_Panel,
]


def register():
    # Register each class in the list
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.planar_properties = bpy.props.PointerProperty(type=properties.PlanarMapping_Properties)


def unregister():
    # Unregister each class in the list
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # Unregister properties if needed
    del bpy.types.Scene.planar_properties

if __name__ == "__main__":
    register()