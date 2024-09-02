import bpy
import math
from .utils import *

def add_camera(target, distance=10, fix_radian=0.28169203286535016*math.pi, angle=0.0, light_distance = 10, light_energy = 200, x_shift = 0, y_shift = 0):
    # camera cal
    location_z = distance*math.sin(fix_radian)
    distance_xy = distance*math.cos(fix_radian)
    location_x = distance_xy * math.sin((-angle - 180) / 180 * math.pi) + x_shift
    location_y = distance_xy * math.cos((-angle - 180) / 180 * math.pi) + y_shift

    # add light

    light_data = bpy.data.lights.new("light", type="SUN")
    light = bpy.data.objects.new("light", light_data)
    bpy.context.collection.objects.link(light)
    light.location = (0.3*light_distance, -0.4*light_distance, 0.5*light_distance)
    light.data.energy = light_energy

    # add camera
    cam_dat = bpy.data.cameras.new('camera')
    cam = bpy.data.objects.new('camera', cam_dat)
    cam.location = (location_x, location_y, location_z)
    constraint = cam.constraints.new(type='TRACK_TO')
    constraint.target = target

    bpy.context.collection.objects.link(cam)

    return cam

def add_workbench_camera(target, view_port = TOPFRONT, distance = 10, x_shift = 0, y_shift = 0):
    if view_port == TOP:
        fix_radian = math.pi / 2
        angle = 0
    elif view_port == BOTTOM:
        fix_radian = - math.pi / 2
        angle = 0
    elif view_port == LEFT:
        fix_radian = 0
        angle = - 90
    elif view_port == RIGHT:
        fix_radian = 0
        angle = 90
    elif view_port == FRONT:
        fix_radian = 0
        angle = 0
    elif view_port == BACK:
        fix_radian = 0
        angle = 180
    elif view_port == TOPFRONT:
        fix_radian = 0.28169203286535016*math.pi
        angle = 0
    else:
        raise Exception("undefined view_port.")

    # camera cal
    location_z = distance * math.sin(fix_radian)
    distance_xy = distance * math.cos(fix_radian)
    location_x = distance_xy * math.sin((-angle - 180) / 180 * math.pi) + x_shift
    location_y = distance_xy * math.cos((-angle - 180) / 180 * math.pi) + y_shift

    # add camera
    cam_dat = bpy.data.cameras.new('camera')
    cam = bpy.data.objects.new('camera', cam_dat)
    cam.location = (location_x, location_y, location_z)
    constraint = cam.constraints.new(type='TRACK_TO')
    constraint.target = target

    bpy.context.collection.objects.link(cam)

    return cam