import bpy
import math
from bpycanvas import *

if __name__ == "__main__":
    start_blender()

    # add bend
    mzi_mesh = CouplerMZIMesh(start_point=Point(-30, 5), layer_num=4,
                              phase_shifter_length=2, interval_length=0.2, coupling_length=0.18, coupling_gap=0.2,
                              width=0.2, radius=0.5, z_start=-0.11, z_end=0.11, material=Si)
    mzi_mesh_obj = mzi_mesh.draw()

    mzi_mesh.add_heater(heater_width=0.4)

    cam = add_workbench_camera(mzi_mesh_obj, view_port=TOPFRONT, distance=30)
    workbench_render('./images/test.png', cam)

    save_blender("./test.blend")


