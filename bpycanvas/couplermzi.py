import bpy
from .waveguide import Waveguide
from .sbend import SBend, ASBend
from .filledpattern import Rectangle
from .utils import Point, HORIZONTAL, VERTICAL
from . doubleconnector import  DoubleBendConnector
from .material import TransparentGold

class PhaseShifter:
    def __init__(self, start_point, phase_shifter_length, width, interval_length=10, z_start = None, z_end = None,
                 material=None, rename = None):
        self.start_point = start_point
        self.phase_shifter_length = phase_shifter_length
        self.width = width
        self.interval_length = interval_length
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename

        # left waveguide
        self.left_waveguide = Waveguide(self.start_point, self.start_point+(self.interval_length, 0), width=self.width,
                                        z_start=self.z_start, z_end=self.z_end, material=self.material, rename=self.rename)

        # phase shifter waveguide
        self.phase_shifter_waveguide = Waveguide(self.left_waveguide.get_end_point(),
                                                 self.left_waveguide.get_end_point() + (self.phase_shifter_length, 0),
                                                 width=self.width, z_start=self.z_start, z_end=self.z_end, material=self.material,
                                                 rename=self.rename)

        # right waveguide
        self.right_waveguide = Waveguide(self.phase_shifter_waveguide.get_end_point(),
                                         self.phase_shifter_waveguide.get_end_point() + (self.interval_length, 0),
                                         width=self.width, z_start=self.z_start, z_end=self.z_end, material=self.material,
                                         rename=self.rename)

    def draw(self):
        ps_obj_1 = self.left_waveguide.draw()
        ps_obj_2 = self.phase_shifter_waveguide.draw()
        ps_obj_3 = self.right_waveguide.draw()
        bpy.ops.object.select_all(action='DESELECT')
        ps_obj_1.select_set(True)
        ps_obj_2.select_set(True)
        ps_obj_3.select_set(True)
        bpy.context.view_layer.objects.active = ps_obj_3
        bpy.ops.object.join()
        ps = bpy.context.object
        return ps

    def add_heater(self, heater_width =2, z_start=0.11, z_end=0.21, material=TransparentGold):
        heater = Waveguide(self.phase_shifter_waveguide.get_start_point(), self.phase_shifter_waveguide.get_end_point(),
                           width=heater_width, z_start=z_start, z_end=z_end, material=material)
        heater.draw()

    def get_left_pad_point(self, heater_width = 2):
        return self.phase_shifter_waveguide.get_start_point() + (heater_width / 2, 20)

    def get_right_pad_point(self, heater_width = 2):
        return self.phase_shifter_waveguide.get_end_point() + (-heater_width/2, 20)

    def get_start_point(self):
        return self.left_waveguide.get_start_point()

    def get_end_point(self):
        return self.right_waveguide.get_end_point()

class CouplerMZI:
    def __init__(self, start_point, phase_shifter_length, coupling_length, coupling_gap, width,
                 radius, interval_length=10, z_start = None, z_end = None,
                 material=None, rename = None):
        self.start_point = start_point
        self.phase_shifter_length = phase_shifter_length
        self.coupling_length = coupling_length
        self.coupling_gap = coupling_gap
        self.width = width
        self.radius = radius
        self.interval_length = interval_length
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename

        # input bend upper
        self.input_bend_upper = SBend(start_point=self.start_point,
                                      end_point=self.start_point + (radius * 2, -radius * 2),
                                      width=self.width, z_start=self.z_start, z_end=self.z_end, material=self.material,
                                      rename=self.rename)

        # left coupler
        self.left_coupler_upper_wg = Waveguide(start_point=self.input_bend_upper.get_end_point(),
                                               end_point=self.input_bend_upper.get_end_point() + (
                                               self.coupling_length, 0),
                                               width=self.width, z_start=self.z_start, z_end=self.z_end,
                                               material=self.material,
                                               rename=self.rename)

        self.left_coupler_lower_wg = Waveguide(
            self.left_coupler_upper_wg.get_start_point() + (0, - self.width - self.coupling_gap),
            self.left_coupler_upper_wg.get_end_point() + (0, - self.width - self.coupling_gap),
            width=self.width, z_start=self.z_start, z_end=self.z_end, material=self.material,
            rename=self.rename)

        # left coupler upper bend
        self.left_coupler_upper_bend = ASBend(start_point=self.left_coupler_upper_wg.get_end_point(),
                                              end_point=self.left_coupler_upper_wg.get_end_point() + (
                                              radius * 2, radius * 2),
                                              width=self.width, z_start=self.z_start, z_end=self.z_end,
                                              material=self.material,
                                              rename=self.rename)

        # left coupler lower bend
        self.left_coupler_lower_bend = SBend(start_point=self.left_coupler_lower_wg.get_end_point(),
                                             end_point=self.left_coupler_lower_wg.get_end_point() + (
                                             radius * 2, -radius * 2),
                                             width=self.width, z_start=self.z_start,
                                             z_end=self.z_end, material=self.material, rename=self.rename
                                             )

        # input bend lower
        self.input_bend_lower = ASBend(
            start_point=self.left_coupler_lower_wg.get_start_point() + (-radius * 2, -radius * 2),
            end_point=self.left_coupler_lower_wg.get_start_point(), width=self.width,
            z_start=self.z_start,
            z_end=self.z_end, material=self.material, rename=self.rename)

        # phase shifter
        self.phase_shifter = PhaseShifter(start_point=self.left_coupler_upper_bend.get_end_point(),
                                          phase_shifter_length=self.phase_shifter_length,
                                          width=self.width, interval_length=self.interval_length, z_start=self.z_start,
                                          z_end=self.z_end, material=self.material, rename=self.rename)

        # right coupler upper bend
        self.right_coupler_upper_bend = SBend(start_point=self.phase_shifter.get_end_point(),
                                              end_point=self.phase_shifter.get_end_point() + (radius * 2, -radius * 2),
                                              width=self.width, z_start=self.z_start, z_end=self.z_end,
                                              material=self.material,
                                              rename=self.rename)

        # right coupler upper waveguide
        self.right_coupler_upper_wg = Waveguide(start_point=self.right_coupler_upper_bend.get_end_point(),
                                                end_point=self.right_coupler_upper_bend.get_end_point() + (
                                                self.coupling_length, 0),
                                                width=self.width, z_start=self.z_start, z_end=self.z_end,
                                                material=self.material,
                                                rename=self.rename)

        self.right_coupler_lower_wg = Waveguide(
            self.right_coupler_upper_wg.get_start_point() + (0, - self.width - self.coupling_gap),
            self.right_coupler_upper_wg.get_end_point() + (0, - self.width - self.coupling_gap),
            width=self.width, z_start=self.z_start, z_end=self.z_end, material=self.material,
            rename=self.rename)

        # right coupler lower bend
        self.right_coupler_lower_bend = ASBend(
            start_point=self.right_coupler_lower_wg.get_start_point() + (-radius * 2, -radius * 2),
            end_point=self.right_coupler_lower_wg.get_start_point(), width=self.width,
            z_start=self.z_start,
            z_end=self.z_end, material=self.material, rename=self.rename)

        # waveguide
        self.waveguide = Waveguide(start_point=self.left_coupler_lower_bend.get_end_point(),
                                   end_point=self.right_coupler_lower_bend.get_start_point(),
                                   width=self.width, z_start=self.z_start, z_end=self.z_end, material=self.material,
                                   rename=self.rename)

        # output bend upper
        self.output_bend_upper = ASBend(start_point=self.right_coupler_upper_wg.get_end_point(),
                                        end_point=self.right_coupler_upper_wg.get_end_point() + (
                                            radius * 2, radius * 2),
                                        width=self.width, z_start=self.z_start,
                                        z_end=self.z_end, material=self.material, rename=self.rename
                                        )

        # output bend lower
        self.output_bend_lower = SBend(start_point=self.right_coupler_lower_wg.get_end_point(),
                                       end_point=self.right_coupler_lower_wg.get_end_point() + (
                                       radius * 2, -radius * 2),
                                       width=self.width, z_start=self.z_start,
                                       z_end=self.z_end, material=self.material, rename=self.rename
                                       )

    def draw(self):
        bpy_obj_list = []
        bpy_obj_list.append(self.input_bend_upper.draw())
        bpy_obj_list.append(self.left_coupler_upper_bend.draw())
        bpy_obj_list.append(self.left_coupler_lower_bend.draw())
        bpy_obj_list.append(self.left_coupler_upper_wg.draw())
        bpy_obj_list.append(self.left_coupler_lower_wg.draw())
        bpy_obj_list.append(self.phase_shifter.draw())
        bpy_obj_list.append(self.output_bend_upper.draw())
        bpy_obj_list.append(self.waveguide.draw())
        bpy_obj_list.append(self.right_coupler_upper_wg.draw())
        bpy_obj_list.append(self.right_coupler_lower_wg.draw())
        bpy_obj_list.append(self.right_coupler_upper_bend.draw())
        bpy_obj_list.append(self.right_coupler_lower_bend.draw())
        bpy_obj_list.append(self.input_bend_lower.draw())
        bpy_obj_list.append(self.output_bend_lower.draw())
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy_obj_list:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = bpy_obj_list[7]
        bpy.ops.object.join()
        mzi = bpy.context.object
        return mzi

    def add_heater(self, heater_width=2, z_start=0.11, z_end=0.21, material=TransparentGold):
        self.phase_shifter.add_heater(heater_width, z_start, z_end, material)

    def get_left_pad_point(self, heater_width=2):
        return self.phase_shifter.get_left_pad_point(heater_width)

    def get_right_pad_point(self, heater_width=2):
        return self.phase_shifter.get_right_pad_point(heater_width)

    def get_start_point(self):
        return self.start_point

    def get_input_point(self):
        return self.start_point

    def get_through_point(self):
        return self.output_bend_upper.get_end_point()

    def get_drop_point(self):
        return self.input_bend_lower.get_start_point()

    def get_add_point(self):
        return self.output_bend_lower.get_end_point()

class CouplerMZIHalfWaveguide:
    def __init__(self, start_point, phase_shifter_length, coupling_length, coupling_gap, width,
                 radius, interval_length=10, z_start = None, z_end = None,
                 material=None, rename = None):
        self.start_point = start_point
        self.phase_shifter_length = phase_shifter_length
        self.coupling_length = coupling_length
        self.coupling_gap = coupling_gap
        self.width = width
        self.radius = radius
        self.interval_length = interval_length
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename

        # input bend upper
        self.input_bend_upper = SBend(start_point=self.start_point, end_point=self.start_point + (radius*2, -radius*2),
                                      width=self.width, z_start=self.z_start, z_end=self.z_end, material=self.material,
                                      rename=self.rename)

        # left coupler
        self.left_coupler_upper_wg = Waveguide(start_point=self.input_bend_upper.get_end_point(),
                                                  end_point=self.input_bend_upper.get_end_point() + (self.coupling_length, 0),
                                               width=self.width, z_start=self.z_start, z_end=self.z_end, material=self.material,
                                      rename=self.rename)

        # left coupler upper bend
        self.left_coupler_upper_bend = ASBend(start_point=self.left_coupler_upper_wg.get_end_point(),
                                        end_point=self.left_coupler_upper_wg.get_end_point() + (radius*2, radius*2),
                                        width=self.width, z_start=self.z_start, z_end=self.z_end, material=self.material,
                                      rename=self.rename)

        # phase shifter
        self.phase_shifter = PhaseShifter(start_point=self.left_coupler_upper_bend.get_end_point(),
                                          phase_shifter_length=self.phase_shifter_length,
                                          width=self.width, interval_length=self.interval_length, z_start=self.z_start,
                                          z_end=self.z_end, material=self.material, rename=self.rename)


        # right coupler upper bend
        self.right_coupler_upper_bend = SBend(start_point=self.phase_shifter.get_end_point(),
                                        end_point=self.phase_shifter.get_end_point() + (radius*2, -radius*2),
                                        width=self.width, z_start=self.z_start, z_end=self.z_end, material=self.material,
                                      rename=self.rename)

        # right coupler upper waveguide
        self.right_coupler_upper_wg =  Waveguide(start_point=self.right_coupler_upper_bend.get_end_point(),
                                                  end_point=self.right_coupler_upper_bend.get_end_point() + (self.coupling_length, 0),
                                               width=self.width, z_start=self.z_start, z_end=self.z_end, material=self.material,
                                      rename=self.rename)

        # output bend upper
        self.output_bend_upper = ASBend(start_point=self.right_coupler_upper_wg.get_end_point(),
                                       end_point=self.right_coupler_upper_wg.get_end_point() + (
                                       radius * 2, radius * 2),
                                       width=self.width, z_start=self.z_start,
                                       z_end=self.z_end, material=self.material, rename=self.rename
                                       )

        # outer phase shifter
        self.outer_phase_shifter = PhaseShifter(start_point=self.output_bend_upper.get_end_point(),
                                          phase_shifter_length=self.phase_shifter_length,
                                          width=self.width, interval_length=self.interval_length, z_start=self.z_start,
                                          z_end=self.z_end, material=self.material, rename=self.rename)

    def draw(self):
        bpy_obj_list = []
        bpy_obj_list.append(self.input_bend_upper.draw())
        bpy_obj_list.append(self.left_coupler_upper_bend.draw())
        bpy_obj_list.append(self.left_coupler_upper_wg.draw())
        bpy_obj_list.append(self.phase_shifter.draw())
        bpy_obj_list.append(self.output_bend_upper.draw())
        bpy_obj_list.append(self.right_coupler_upper_wg.draw())
        bpy_obj_list.append(self.right_coupler_upper_bend.draw())
        bpy_obj_list.append(self.outer_phase_shifter.draw())
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy_obj_list:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = bpy_obj_list[3]
        bpy.ops.object.join()
        wg = bpy.context.object
        return wg


    def get_start_point(self):
        return self.start_point

    def get_end_point(self):
        return self.outer_phase_shifter.get_end_point()

class CouplerMZIPlusPhaseShifter:
    def __init__(self, start_point, phase_shifter_length, coupling_length, coupling_gap, width,
                 radius, interval_length=10, z_start=None, z_end=None,
                 material=None, rename=None):
        self.start_point = start_point
        self.phase_shifter_length = phase_shifter_length
        self.coupling_length = coupling_length
        self.coupling_gap = coupling_gap
        self.width = width
        self.radius = radius
        self.interval_length = interval_length
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename

        self.mzi = CouplerMZI(start_point=self.start_point, phase_shifter_length=self.phase_shifter_length,
                              coupling_length=self.coupling_length, coupling_gap=self.coupling_gap,
                              width=self.width, radius=self.radius, interval_length=self.interval_length,
                              z_start=self.z_start, z_end=self.z_end, material=self.material, rename=self.rename)

        self.phase_shifter = PhaseShifter(self.mzi.get_through_point(), phase_shifter_length=self.phase_shifter_length,
                                          width=self.width, interval_length=self.interval_length,z_start=self.z_start,
                                          z_end=self.z_end, material=self.material, rename=self.rename)

        self.waveguide = Waveguide(self.mzi.get_add_point(), self.mzi.get_add_point() + (self.phase_shifter_length +
                            2*self.interval_length, 0),width=self.width, z_start=self.z_start,
                                          z_end=self.z_end, material=self.material, rename=self.rename)

    def draw(self):
        bpy_obj_list = []
        bpy_obj_list.append(self.mzi.draw())
        bpy_obj_list.append(self.phase_shifter.draw())
        bpy_obj_list.append(self.waveguide.draw())
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy_obj_list:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = bpy_obj_list[0]
        bpy.ops.object.join()
        mzi = bpy.context.object
        return mzi


    def add_heater(self, heater_width=2, z_start=0.11, z_end=0.21, material=TransparentGold):
        self.mzi.add_heater(heater_width, z_start, z_end, material)
        self.phase_shifter.add_heater(heater_width, z_start, z_end, material)

    def get_start_point(self):
        return self.start_point

    def get_input_point(self):
        return self.start_point

    def get_through_point(self):
        return self.phase_shifter.get_end_point()

    def get_drop_point(self):
        return self.mzi.get_drop_point()

    def get_add_point(self):
        return self.waveguide.get_end_point()

class CouplerMZIMesh:
    def __init__(self, start_point, layer_num, phase_shifter_length, coupling_length, coupling_gap, width,
                 radius, interval_length=10, z_start = None, z_end = None,
                 material=None, rename = None):

        self.start_point = start_point
        self.layer_num = layer_num
        self.phase_shifter_length = phase_shifter_length
        self.coupling_length = coupling_length
        self.coupling_gap =coupling_gap
        self.width = width
        self.radius = radius
        self.interval_length = interval_length
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename

        self.node_list = []
        self.bend_waveguide_list = []

        self.x_interval = self.radius*8 + self.coupling_length*2 + self.interval_length*4 + self.phase_shifter_length*2
        self.y_interval = self.radius*4 + self.coupling_gap + self.width

        for row in range(0, 2*self.layer_num - 1):
            row_node_list = []
            for col in range(0, self.layer_num):
                if row % 2 == 0:
                    mzi = CouplerMZIPlusPhaseShifter(start_point=self.start_point + (2*self.x_interval*col, -self.y_interval*row),
                                                     phase_shifter_length=self.phase_shifter_length,
                                                     coupling_length=self.coupling_length, coupling_gap=self.coupling_gap,
                                                     width=self.width, radius=self.radius, interval_length=self.interval_length,
                                                     z_start=self.z_start, z_end=self.z_end, material=self.material,
                                                     rename=self.rename)
                    row_node_list.append(mzi)
                else:
                    mzi = CouplerMZIPlusPhaseShifter(start_point=self.start_point + (self.x_interval*(1 + 2*col), -self.y_interval*row),
                                                     phase_shifter_length=self.phase_shifter_length,
                                                     coupling_length=self.coupling_length, coupling_gap=self.coupling_gap,
                                                     width=self.width, radius=self.radius, interval_length=self.interval_length,
                                                     z_start=self.z_start, z_end=self.z_end, material=self.material,
                                                     rename=self.rename)
                    row_node_list.append(mzi)

                    if row == 1 : # put upper mzi like waveguide
                        bend_waveguide = CouplerMZIHalfWaveguide(start_point=self.start_point + (self.x_interval*(1 + 2*col), 0),
                                                     phase_shifter_length=self.phase_shifter_length,
                                                     coupling_length=self.coupling_length, coupling_gap=self.coupling_gap,
                                                     width=self.width, radius=self.radius, interval_length=self.interval_length,
                                                     z_start=self.z_start, z_end=self.z_end, material=self.material,
                                                     rename=self.rename)
                        self.bend_waveguide_list.append(bend_waveguide)

                    if row == 2*self.layer_num - 3: # put lower mzi like waveguide
                        bend_waveguide = CouplerMZIHalfWaveguide(
                            start_point=self.start_point + (self.x_interval * (1 + 2 * col),  -self.y_interval*(row+2)),
                            phase_shifter_length=self.phase_shifter_length,
                            coupling_length=self.coupling_length, coupling_gap=self.coupling_gap,
                            width=self.width, radius=self.radius, interval_length=self.interval_length,
                            z_start=self.z_start, z_end=self.z_end, material=self.material,
                            rename=self.rename)
                        self.bend_waveguide_list.append(bend_waveguide)

            self.node_list.append(row_node_list)

    def draw(self):
        bpy_obj_list = []
        for row_node_list in self.node_list:
            for mzi in row_node_list:
                bpy_obj_list.append(mzi.draw())

        for bend_waveguide in self.bend_waveguide_list:
            bpy_obj_list.append(bend_waveguide.draw())

        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy_obj_list:
            obj.select_set(True)

        bpy.context.view_layer.objects.active = bpy_obj_list[self.layer_num*int(len(self.node_list)/2 - 1) +
                                                             int(self.layer_num/2)]
        bpy.ops.object.join()
        mesh = bpy.context.object
        return mesh

    def add_heater(self, heater_width=2, z_start=0.11, z_end=0.21, material=TransparentGold):
        for row_node_list in self.node_list:
            for mzi in row_node_list:
                mzi.add_heater(heater_width, z_start, z_end, material)
