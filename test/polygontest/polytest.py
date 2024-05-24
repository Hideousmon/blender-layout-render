import bpy
import math
from bpycanvas import *

if __name__ == "__main__":
    start_blender()

    # add poly
    vertices = [(1.0, 1.0), (1.0, -1.0), (-1.0, -1.0), (-1.0, 1.0)]
    poly = Polygon(vertices, z_start=-0.11, z_end=0.11, material=Si)
    poly_obj = poly.draw()

    cam = add_workbench_camera(poly_obj, view_port=TOPFRONT)
    workbench_render('./images/test.png', cam)

    save_blender("./test.blend")


