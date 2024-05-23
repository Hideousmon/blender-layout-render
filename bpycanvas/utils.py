import bpy
import os
import math
import mathutils

VERTICAL = 0
HORIZONTAL = 1
TOP = 0
BOTTOM = 1
FRONT = 2
BACK = 3
LEFT = 4
RIGHT = 5
TOPFRONT = 6

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
    scene.render.filepath = filename
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
    scene.render.filepath = filename
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y

    bpy.ops.render.render(write_still=True)

class Point:
    """
    Point Definition in SPLayout. Point is the basic unit that describe the locations of all the
    components in SPLayout.

    Parameters
    ----------
    x : float
        The x coordinate of a point.
    y : float
        The y coordinate of a point.

    Notes
    -----
    By overloading operators, the Point object can do calculations with Point object and Tuples, the available operations are:
    Point == Point
    Point + Point
    Point + Tuple
    Point - Point
    Point - Tuple
    Point / float
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):

        if (type(other) != Point):
            return False
        else:
            return (self.x == other.x) and (self.y == other.y)

    def to_tuple(self):
        """
        Convert Point into Tuple.

        Returns
        -------
        out : Tuple
            (x,y).
        """
        return (self.x, self.y)

    def get_percent_point(self,others,percent = 0.5):
        """
        Derive the point on the connection line of the point and the other point.

        Parameters
        ----------
        others : Point
            Another end of the line.
        percent : float
            The percent from the original point to the end of the line (0~1).

        Returns
        -------
        out : Point
            The desired point.
        """
        return Point( self.x + (others.x - self.x)*percent,  self.y+ (others.y - self.y)*percent)

    def get_relative_radian(self,other): ## ! -pi to pi
        """
        Derive the relative radian with another point as a circle center point.

        Parameters
        ----------
        others : Point
            The center of the circle.

        Returns
        -------
        out : float
            The desired radian (radian,  -pi to pi).
        """
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
    """
    Automatically convert tuple to Point.

    Parameters
    ----------
    input_tuple : tuple or Point
        The data to be converted.

    Returns
    -------
    output_point : Point
        Converted Point.
    """
    if type(input_tuple) == tuple and len(input_tuple) == 2:
        output_point = Point(input_tuple[0],input_tuple[1])
    elif type(input_tuple) == Point:
        output_point = input_tuple
    elif type(input_tuple) == type(None):
        output_point = None
    else:
        raise Exception("Wrong data type input!")
    return output_point