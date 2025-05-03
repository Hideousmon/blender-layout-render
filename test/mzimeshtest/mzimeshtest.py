import bpy
import math
from bpycanvas import *

if __name__ == "__main__":
    Si = {  # 0,0,255
        "Name": "BrownArrow",
        "Base Color": [0.509, 0.372, 0.686, 1],
        "Roughness": 0.2,
        "Metallic": 1.0,
        "IOR": 1.0,
        "Alpha": 1,
        "Diffusion Color": [0.509, 0.372, 0.686, 0.9],
    }

    SiO2 = {
        "Name": "SiO2",
        "Base Color": [1.0, 1.0, 1.0, 1],
        "Roughness": 0.1,
        "Metallic": 0.0,
        "IOR": 1.0,
        "Alpha": 1.0,
        "Diffusion Color": [1.0, 1.0, 1.0, 0.1],
    }

    HeaterMaterial = {
        "Name": "Heater",
        "Base Color": [0.5, 0.5, 0.5, 1],
        "Roughness": 0.5,
        "Metallic": 0.5,
        "IOR": 1.0,
        "Alpha": 0.7,
        "Diffusion Color": [0.5, 0.5, 0.5, 0.7],
    }

    start_blender()

    # add bend
    mzi_mesh = CouplerMZIMesh(start_point=Point(-30, 5), layer_num=2,
                              phase_shifter_length=2, interval_length=0.2, coupling_length=0.18, coupling_gap=0.2,
                              width=0.2, radius=0.5, z_start=-0.11, z_end=0.11, material=Si)
    mzi_mesh_obj = mzi_mesh.draw()

    mzi_mesh.add_heater(heater_width=0.4)

    cam = add_workbench_camera(mzi_mesh_obj, view_port=TOPFRONT, distance=30)
    workbench_render('./images/test.png', cam)

    save_blender("./test.blend")


