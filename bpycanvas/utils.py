import bpy
import os
import math

VERTICAL = 0
HORIZONTAL = 1
TOP = 0
BOTTOM = 1
FRONT = 2
BACK = 3
LEFT = 4
RIGHT = 5
TOPFRONT = 6
UP = 90
DOWN = 270

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

def start_blender_with_loading(loading_absolute_path):
    bpy.ops.wm.open_mainfile(filepath=loading_absolute_path)

def save_blender(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        bpy.ops.wm.save_mainfile(filepath=filepath)
    else:
        bpy.ops.wm.save_mainfile(filepath=filepath)
    bpy.ops.wm.quit_blender()

def cycles_render(filename, scene_cam, resolution_x = 480, resolution_y = 320, use_cuda = True):
    bpy.context.window_manager.windows.update()
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.film_transparent = True
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
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.filepath = os.path.abspath(filename)
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y

    bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)

def workbench_render(filename, scene_cam, resolution_x = 480, resolution_y = 320, color_mode = 'RGBA'):
    bpy.context.window_manager.windows.update()
    bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.camera = scene_cam

    scene = bpy.context.scene
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = color_mode
    scene.render.filepath = os.path.abspath(filename)
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y

    bpy.ops.render.render(write_still=True)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):

        if (type(other) != Point):
            return False
        else:
            return (self.x == other.x) and (self.y == other.y)

    def to_tuple(self):

        return (self.x, self.y)

    def get_percent_point(self,others,percent = 0.5):
        return Point( self.x + (others.x - self.x)*percent,  self.y+ (others.y - self.y)*percent)

    def get_relative_radian(self,other): ## ! -pi to pi
        radian = math.atan( (self.y - other.y)/(self.x - other.x))
        return radian

    def __add__(self, other):
        if (type(other) == Point):
            return Point(self.x + other.x,self.y + other.y)
        elif (type(other) == tuple):
            return Point(self.x + other[0],self.y + other[1])
        else:
            raise Exception("Wrong data type!")

    def __sub__(self, other):
        if (type(other) == Point):
            return Point(self.x - other.x,self.y - other.y)
        elif (type(other) == tuple):
            return Point(self.x - other[0],self.y - other[1])
        else:
            raise Exception("Wrong data type!")

    def __truediv__(self, num):
        return Point(self.x /num, self.y/num)

    def __mul__(self, num):
        return Point(self.x * num, self.y * num)

    def __str__(self):
        return ("({},{})".format(self.x, self.y))

def tuple_to_point(input_tuple):
    if type(input_tuple) == tuple and len(input_tuple) == 2:
        output_point = Point(input_tuple[0],input_tuple[1])
    elif type(input_tuple) == Point:
        output_point = input_tuple
    elif type(input_tuple) == type(None):
        output_point = None
    else:
        raise Exception("Wrong data type input!")
    return output_point