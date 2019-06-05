bl_info = {
	"name": "Nexus Edit Library",
	"author": "Nexus Studio",
	"version": (0, 1, 0),
	"blender": (2, 80, 0),
	"location": "View 3D > N menu",
	"description": "Reload linked object by button",
	"warning": "",
	"wiki_url": "https://github.com/Hichigo/NexusEditLibrary",
	"category": "Object"
	}

import bpy
import os
import subprocess


class EditLibraryOperator(bpy.types.Operator):
    """" Open file linked object """
    bl_idname = "object.edit_library"
    bl_label = "Edit Library"

    def execute(self, context):
        file_path = context.active_object.instance_collection.library.filepath

        #open file in new window
        subprocess.Popen([bpy.app.binary_path, bpy.path.abspath(file_path)])

        return {'FINISHED'}


class OpenFolderLibraryOperator(bpy.types.Operator):
    bl_idname = "object.open_folder_library"
    bl_label = "Open Folder Library"

    def execute(self, context):

        file_path = os.path.split(context.active_object.instance_collection.library.filepath)[0] # get folder path

        bpy.ops.wm.path_open(filepath=file_path)
        return {'FINISHED'}


class ReloadLibraryOperator(bpy.types.Operator):
    bl_idname = "object.reload_library"
    bl_label = "Reload Library"

    def execute(self, context):
        file_path = context.active_object.instance_collection.library.filepath
        lib_name = os.path.basename(file_path)
        bpy.data.libraries[lib_name].reload()
        return {'FINISHED'}


class EditLibraryPanel(bpy.types.Panel):

    bl_label = "Nexus Edit Library"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Nexus"


    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT")

    def draw(self, context):
        layout = self.layout

        if context.active_object.instance_collection is not None:
            file_path = context.active_object.instance_collection.library.filepath

            layout.operator("object.edit_library", text="Edit Library", icon="LINK_BLEND")

            layout.label(text=file_path)
        
            layout.operator("object.open_folder_library", text="Open Folder Library", icon="FILE_FOLDER")
            layout.operator("object.reload_library", text="Reload Library", icon="FILE_REFRESH")
        else:
            layout.label(text="No active library!")


classes = (
    EditLibraryOperator,
    OpenFolderLibraryOperator,
    ReloadLibraryOperator,
    EditLibraryPanel
)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)

if __name__ == "__main__":
	register()
