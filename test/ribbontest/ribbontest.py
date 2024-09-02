import bpy
import math
from bpycanvas import *

if __name__ == "__main__":
    start_blender()

    ribbon = Ribbon([(0, 0, 0), (2, 2, 1), (4, 3, 0), (6, 2, -1), (8, 0, 0)], width=0.2, material=Si)
    ribbon_obj = ribbon.draw()

    cam = add_workbench_camera(ribbon_obj, view_port=TOPFRONT, distance=30)
    workbench_render('./images/test.png', cam)

    save_blender("./test.blend")


