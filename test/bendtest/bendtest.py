import bpy
import math
from bpycanvas import *

if __name__ == "__main__":
    start_blender()

    # add bend
    poly = Bend(center_point=Point(0, 0), radius=5, width=0.5, start_radian=0, end_radian=math.pi*2, z_start=-0.11, z_end=0.11, material=Si)
    poly_obj = poly.draw()

    cam = add_workbench_camera(poly_obj, view_port=TOPFRONT, distance=30)
    workbench_render('./images/test.png', cam)

    save_blender("./test.blend")


