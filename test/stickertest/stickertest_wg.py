import bpy
import math
from bpycanvas import *

if __name__ == "__main__":
    start_blender()

    wg = Waveguide(Point(-2, 0), Point(2, 0), width=1, z_start=-0.11, z_end=0.11, material=Si)
    wg_bpy = wg.draw()

    sp = StickerPlane(Point(0,0), image_path='D:\\GithubProjects\\blender-pyscripts-learning\\test\\stickertest\\images\\test1.png',
                      width=3, height=1.2, z_center=0.111)
    sp_bpy = sp.draw()

    cam = add_camera(sp_bpy, angle=0, distance=8, light_distance=10, light_energy=10)

    cycles_render('D:\\GithubProjects\\blender-pyscripts-learning\\test\\stickertest\\images\\test.png', cam,
           resolution_x=1024, resolution_y=768)

    save_blender("./test.blend")