import bpy
import os

def start_blender():
    current_folder_path = os.path.dirname(os.path.realpath(__file__))
    bpy.ops.wm.open_mainfile(filepath=current_folder_path + "/base.blend")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for material in bpy.data.materials:
        if not material.users:
            bpy.data.materials.remove(material)

    for texture in bpy.data.textures:
        if not texture.users:
            bpy.data.textures.remove(texture)

def save_blender(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        bpy.ops.wm.save_mainfile(filepath=filepath)
    else:
        bpy.ops.wm.save_mainfile(filepath=filepath)
    bpy.ops.wm.quit_blender()

def render(filename, scene_cam, resolution_x = 480, resolution_y = 320, use_cuda = True):
    bpy.context.scene.render.engine = 'CYCLES'
    if use_cuda:
        bpy.context.scene.cycles.device = 'GPU'
        cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
        if hasattr(cycles_prefs, 'get_devices'):
            cycles_prefs.get_devices()
        bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
        for device in cycles_prefs.devices:
            if device.type == 'CUDA':
                device.use = True
            else:
                device.use = False
            print(f"Device: {device.name}, Type: {device.type}, Use: {device.use}")

    scene = bpy.context.scene
    scene.camera = scene_cam
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = filename
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y

    bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)