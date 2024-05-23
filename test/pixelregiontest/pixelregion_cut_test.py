import bpy
import math
from bpycanvas import *
import numpy as np

if __name__ == "__main__":
    start_blender()

    base = Rectangle(Point(0,0), width=8, z_start=-0.11, z_end=0.11, material=Si)
    base_obj = base.draw()

    # pixel region
    mask = np.ones((20, 20))
    # cr = RectanglePixelsRegion(bottom_left_corner_point=Point(-4,-4), top_right_corner_point=Point(4, 4),
    #                         pixel_x_length=0.1, pixel_y_length=0.1, z_start=-0.11, z_end=0.11, material=Si, matrix_mask=mask)
    # cr_obj = cr.draw(np.ones(400))

    cr = CirclePixelsRegion(bottom_left_corner_point=Point(-4,-4), top_right_corner_point=Point(4, 4),
                            pixel_radius=0.1, z_start=-0.11, z_end=0.11, material=Si, matrix_mask=mask)
    cr_obj = cr.draw(np.ones(400))

    # cut(base_obj, cr_obj)

    cam = add_workbench_camera(base_obj, view_port=TOPFRONT, distance=15)
    workbench_render('D:/GithubProjects/blender-pyscripts-learning/test/pixelregiontest/images/test.png', cam, color_mode='BW')

    save_blender("./test.blend")
