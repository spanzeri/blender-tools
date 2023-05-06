import bpy
from . rigging_helpers import (SRT_PT_RiggingHelperPanel, SRT_OT_CreateTargetBone)

bl_info = {
    "name": "Sam's Rigging Helpers",
    "author": "Samuele Panzeri",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3d > Tool",
    "warning": "Use at your own risk",
    "wiki_url": "",
    "category": "Rigging"
}


classes = (
    SRT_PT_RiggingHelperPanel,
    SRT_OT_CreateTargetBone
)


def menu_func(self, context):
    self.layout.operator(SRT_OT_CreateTargetBone.bl_idname)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_edit_armature.append(menu_func)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_edit_armature.remove(menu_func)


if __name__ == "__main__":
    register()
