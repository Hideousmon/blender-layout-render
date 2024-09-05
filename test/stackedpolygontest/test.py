import bpy
import math
from bpycanvas import *
import numpy as np

if __name__ == "__main__":
    start_blender()

    functional_poly = np.load("./polygons/functional_polygons.npy", allow_pickle=True)
    poly_types = np.load("./polygons/polygon_types.npy", allow_pickle=True)

    # add stacked poly
    poly = StackedPolygon(functional_poly, poly_types, z_start=-0.11, z_end=0.11, material=Si)
    poly_obj = poly.draw()

    cam = add_workbench_camera(poly_obj, view_port=TOPFRONT)
    workbench_render('./images/test.png', cam)

    save_blender("./test.blend")


