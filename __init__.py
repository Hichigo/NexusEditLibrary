bl_info = {
	"name": "Nexus Edit Library",
	"author": "Nexus Studio",
	"version": (0, 1, 2),
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


class VIEW3D_OT_OpenFolderLibrary(bpy.types.Operator):
    bl_idname = "object.open_folder_library"
    bl_label = "Open Folder Library"

    def execute(self, context):

        file_path = os.path.split(context.active_object.instance_collection.library.filepath)[0] # get folder path

        bpy.ops.wm.path_open(filepath=file_path)
        return {'FINISHED'}

class VIEW3D_OT_CopyFilePath(bpy.types.Operator):
    bl_idname = "object.copy_file_path"
    bl_label = "Copy File Path"

    def execute(self, context):

        file_path = os.path.split(context.active_object.instance_collection.library.filepath)[0] # get folder path
        bpy.context.window_manager.clipboard = file_path
        self.report({"INFO"}, "PATH COPIED!")

        return {'FINISHED'}


class ReloadLibraryOperator(bpy.types.Operator):
    bl_idname = "object.reload_library"
    bl_label = "Reload Library"

    def execute(self, context):
        file_path = context.active_object.instance_collection.library.filepath
        lib_name = os.path.basename(file_path)
        bpy.data.libraries[lib_name].reload()
        return {'FINISHED'}


class ReplaceCollectionOperator(bpy.types.Operator):
    """ You take 2 objects to change the collection: 1 - with which; 2 - on what """
    bl_idname = "object.replace_collection"
    bl_label = "Replace Collection"

    def execute(self, context):
        active_object = bpy.context.active_object

        active_object.select_set(False)

        bpy.context.selected_objects[0].select_set(True)
        bpy.context.window.view_layer.objects.active = bpy.context.selected_objects[0]

        bpy.ops.object.select_linked(type='DUPGROUP')

        active_object.select_set(True)
        bpy.context.window.view_layer.objects.active = active_object

        bpy.ops.object.make_links_data(type='DUPLICOLLECTION')

        bpy.data.objects.remove(active_object)
        return {'FINISHED'}


class VIEW3D_PT_EditLibrary(bpy.types.Panel):

    bl_label = "Nexus Edit Library"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Nexus"
    bl_options = {"DEFAULT_CLOSED"}


    @classmethod
    def poll(cls, context):
        return (context.mode == "OBJECT")

    def draw(self, context):
        layout = self.layout
        if hasattr(context.active_object, 'instance_collection'):
            if context.active_object.instance_collection is not None:
                file_path = bpy.path.abspath(context.active_object.instance_collection.library.filepath)

                layout.operator("object.edit_library", text="Edit Library", icon="LINK_BLEND")

                row = layout.row()
                row.label(text=file_path)
                row.operator("object.copy_file_path", text="", icon="DUPLICATE")
            
                layout.operator("object.open_folder_library", text="Open Folder Library", icon="FILE_FOLDER")
                layout.operator("object.reload_library", text="Reload Library", icon="FILE_REFRESH")

                layout.operator("object.replace_collection", text="Replace Collection", icon="UV_SYNC_SELECT")
            else:
                layout.label(text="No active library!")


classes = (
    EditLibraryOperator,
    VIEW3D_OT_OpenFolderLibrary,
    VIEW3D_OT_CopyFilePath,
    ReloadLibraryOperator,
    ReplaceCollectionOperator,
    VIEW3D_PT_EditLibrary
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
