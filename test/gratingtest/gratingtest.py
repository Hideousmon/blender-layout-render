import bpy
import math
from bpycanvas import *

if __name__ == "__main__":
    start_blender()

    # add grating
    grating = Grating(start_point=Point(1, 0), z_start=-0.11, z_end=0.11,material=Si, etch_depth=0.22)
    grating_obj = grating.draw()

    cam = add_workbench_camera(grating_obj, view_port=TOPFRONT, distance=100)
    workbench_render('./images/test.png', cam)

    save_blender("./test.blend")


