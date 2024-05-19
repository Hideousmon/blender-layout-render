import bpy
import math

def add_camera(target, distance=10, angle=0.0, light_distance = 10, light_energy = 200):
    # camera cal
    fix_radian = math.atan(0.5)
    location_z = distance*math.sin(fix_radian)
    distance_xy = distance*math.cos(fix_radian)
    location_x = distance_xy * math.sin((-angle - 180) / 180 * math.pi)
    location_y = distance_xy * math.cos((-angle - 180) / 180 * math.pi)

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