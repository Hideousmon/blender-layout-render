import bpy
import os

def start_blender():
    current_folder_path = os.path.dirname(os.path.realpath(__file__))
    bpy.ops.wm.open_mainfile(filepath=current_folder_path + "/base.blend")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def save_blender(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        bpy.ops.wm.save_mainfile(filepath=filepath)
    else:
        bpy.ops.wm.save_mainfile(filepath=filepath)
    bpy.ops.wm.quit_blender()