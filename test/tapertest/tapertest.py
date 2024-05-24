import bpy
import math
from bpycanvas import *

if __name__ == "__main__":
    start_blender()

    # add taper
    taper = Taper(start_point=Point(0, 0), end_point=Point(5, 0),start_width=0.5, end_width=1, z_start=-0.11, z_end=0.11,
                 material=Si)
    taper_obj = taper.draw()

    cam = add_workbench_camera(taper_obj, view_port=TOPFRONT, distance=20)
    workbench_render('./images/test.png', cam)

    save_blender("./test.blend")


