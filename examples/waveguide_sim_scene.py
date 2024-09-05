""" https://github.com/Hideousmon/blender-layout-render """
from bpycanvas import *

if __name__ == "__main__":
    start_blender()

    backgroud = Waveguide(Point(-2, 0), Point(2, 0), width=2, z_start=-0.4, z_end=0.4, material=SiO2)
    backgroud.draw()

    wg = Waveguide(Point(-2, 0), Point(2, 0), width=1, z_start=-0.11, z_end=0.11, material=Si)
    wg_obj = wg.draw()

    arrow = Arrow(Point(-1.8, 0), Point(-1.2, 0), width=0.05, z_start=0.25, z_end=0.25, material=BlueArrow)
    arrow.draw()

    source = Plane(Point(-1.5, 0), width=1.5, height=0.8, z_center=0, material=Source)
    source.draw()

    monitor = Plane(Point(1.5, 0), width=1.5, height=0.8, z_center=0, material=Monitor)
    monitor.draw()

    cam = add_camera(wg_obj, angle=0, distance=8, light_distance=10, light_energy=10)

    cycles_render('./waveguide_sim_scene.png', cam, resolution_x=1920, resolution_y=1080)

    save_blender("./waveguide_sim_scene.blend")