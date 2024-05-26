""" https://github.com/Hideousmon/blender-layout-render """
from bpycanvas import *
import numpy as np

if __name__ == "__main__":
    start_blender()

    start_point = Point(0, 0)
    input_grating = Grating(start_point, z_start=-0.11, z_end=0.11, relative_position=LEFT, wg_width=0.5,
                            etch_depth=0.22, material=Si, scale=0.2)
    input_grating.draw()

    input_wg = Waveguide(input_grating.get_start_point(), input_grating.get_start_point() + (5, 0),
                         width=0.5, z_start=-0.11, z_end=0.11, material=Si)
    input_wg.draw()

    # splitter
    splitter_poly_points = [input_wg.get_end_point() + (0, 0.5 /2),
                            input_wg.get_end_point() + (2, 4),
                            input_wg.get_end_point() + (3, 4),
                            input_wg.get_end_point() + (3, -4),
                            input_wg.get_end_point() + (2, -4),
                            input_wg.get_end_point() + (0, -0.5 /2)]
    splitter_poly = Polygon(splitter_poly_points, z_start=-0.11, z_end=0.11, material=Si)
    splitter_poly.draw()

    inter_wg_1 = Waveguide(input_wg.get_end_point() + (3, 0.75 + 0.5 + 1.5 + 0.5/2),
                           input_wg.get_end_point() + (3, 0.75 + 0.5 + 1.5 + 0.5/2) + (15, 0), width=0.5,
                           z_start=-0.11, z_end=0.11, material=Si)
    inter_wg_1.draw()

    inter_wg_2 = Waveguide(input_wg.get_end_point() + (3, 0.75 + 0.5 / 2),
                           input_wg.get_end_point() + (3, 0.75 + 0.5 / 2) + (15, 0), width=0.5,
                           z_start=-0.11, z_end=0.11, material=Si)
    inter_wg_2_obj = inter_wg_2.draw()

    inter_wg_3 = Waveguide(input_wg.get_end_point() + (3, -0.75 - 0.5 / 2),
                           input_wg.get_end_point() + (3, -0.75 - 0.5 / 2) + (15, 0), width=0.5,
                           z_start=-0.11, z_end=0.11, material=Si)
    inter_wg_3.draw()

    inter_wg_4 = Waveguide(input_wg.get_end_point() + (3, -0.75 - 0.5 - 1.5 - 0.5 / 2),
                           input_wg.get_end_point() + (3, -0.75 - 0.5 - 1.5 - 0.5 / 2) + (15, 0), width=0.5,
                           z_start=-0.11, z_end=0.11, material=Si)
    inter_wg_4.draw()

    start_point_rect_region = inter_wg_2.get_end_point() + (0, -0.5/2 - 0.75)

    rect_region = Waveguide(start_point_rect_region,
                            start_point_rect_region + (8, 0), width=8, z_start=-0.11, z_end=0.11, material=Si)
    rect_region_obj = rect_region.draw()

    # pixel region
    pixels_region_mask_matrix = np.ones((40, 40))
    pnn_pixel_region = CirclePixelsRegion(bottom_left_corner_point=start_point_rect_region + Point(0, -4), material=SiO2,
                                          top_right_corner_point=start_point_rect_region + Point(8, 4), pixel_radius=0.1,
                                          z_start=-0.11, z_end=0.11, matrix_mask=pixels_region_mask_matrix)

    pnn_pixel_obj = pnn_pixel_region.draw(np.ones(40*40))

    # boolean operation (time-consuming)
    # cut(rect_region_obj, pnn_pixel_obj)

    # output waveguide and grating
    output_wg_2 = Waveguide(rect_region.get_end_point(), rect_region.get_end_point() + (5, 0), width=0.5,
                            z_start=-0.11, z_end=0.11, material=Si)
    output_wg_2.draw()

    output_grating_2 = Grating(output_wg_2.get_end_point(), z_start=-0.11, z_end=0.11, etch_depth=0.22, material=Si,
                               scale=0.2)
    output_grating_2.draw()

    output_grating_1 = Grating(output_grating_2.get_start_point() + (0, 8), z_start=-0.11, z_end=0.11, etch_depth=0.22,
                               material=Si, scale=0.2)
    output_grating_1.draw()

    output_grating_3 = Grating(output_grating_2.get_start_point() + (0, -8), z_start=-0.11, z_end=0.11, etch_depth=0.22,
                               material=Si, scale=0.2)
    output_grating_3.draw()

    output_wg_1 = DoubleBendConnector(rect_region.get_end_point() + (0, 2), end_point=output_grating_1.get_start_point(),
                                      width=0.5, z_start=-0.11, z_end=0.11, material=Si, radius=1)
    output_wg_1.draw()

    output_wg_3 = DoubleBendConnector(rect_region.get_end_point() + (0, -2),
                                      end_point=output_grating_3.get_start_point(),
                                      width=0.5, z_start=-0.11, z_end=0.11, material=Si, radius=1)
    output_wg_3.draw()

    phase_shifter_1 = Waveguide(inter_wg_1.get_start_point() + (5, 0), inter_wg_1.get_start_point() + (10, 0),
                                width=1, z_start=0.11, z_end=0.16, material=TransparentGold)
    phase_shifter_1.draw()

    phase_shifter_2 = Waveguide(inter_wg_2.get_start_point() + (5, 0), inter_wg_2.get_start_point() + (10, 0),
                                width=1, z_start=0.11, z_end=0.16, material=TransparentGold)
    phase_shifter_2.draw()

    phase_shifter_3 = Waveguide(inter_wg_3.get_start_point() + (5, 0), inter_wg_3.get_start_point() + (10, 0),
                                width=1, z_start=0.11, z_end=0.16, material=TransparentGold)
    phase_shifter_3.draw()

    phase_shifter_4 = Waveguide(inter_wg_4.get_start_point() + (5, 0), inter_wg_4.get_start_point() + (10, 0),
                                width=1, z_start=0.11, z_end=0.16, material=TransparentGold)
    phase_shifter_4.draw()

    cam = add_workbench_camera(inter_wg_2_obj, view_port=TOPFRONT, distance=85, x_shift=inter_wg_2.get_start_point().x + 7.5)
    workbench_render('./integration_layout_schematic.png', cam, resolution_x=1920, resolution_y=1080)

    save_blender("./integration_layout_schematic.blend")