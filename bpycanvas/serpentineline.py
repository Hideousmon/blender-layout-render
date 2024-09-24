import bpy
from .waveguide import Waveguide
from .doubleconnector import DoubleBendConnector
from .utils import Point, HORIZONTAL, VERTICAL, tuple_to_point
import math

class SerpentineLine:
    def __init__(self, start_point, end_point, length, radius, width, z_start=None, z_end=None, material=None, rename=None):
        self.start_point = tuple_to_point(start_point)
        self.end_point = tuple_to_point(end_point)
        if self.start_point.x != self.end_point.x and self.start_point.y != self.end_point.y:
            raise Exception("Invalid SerpentineLine Parameter!")
        if self.start_point.x == self.end_point.x:  # vertical
            self.distance = abs(self.start_point.y - self.end_point.y)
            self.waveguide_type = VERTICAL
        else:  # horizontal
            self.distance = abs(self.start_point.x - self.end_point.x)
            self.waveguide_type = HORIZONTAL
        self.length = length
        self.radius = radius
        self.width = width
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename
        self.bend_list = []

        self.max_interval = self.radius*math.pi/2
        # calculate segments
        additional_length = self.length - self.distance
        min_additional_length = 2*math.pi*radius - radius*4
        if additional_length < min_additional_length:
            raise Exception("length is too small for the existing radius.")

        self.segments = math.floor((additional_length - 2*math.pi*self.radius + 4*self.radius) /
                              (math.pi*self.radius)) + 1

        if self.distance < self.radius*2*(self.segments+1):
            raise Exception("distance is too small for the true length and existing radius.")

        interval = (additional_length - (
                    2 * math.pi * self.radius + (self.segments - 1) * math.pi * self.radius
                    - 4 * self.radius)) / (self.segments * 2)

        temp_start_point = self.start_point
        # horizontal left to right condition
        if self.waveguide_type == HORIZONTAL and self.start_point.x < self.end_point.x:
            for i in range(0, self.segments):
                if i%2 == 0:
                    temp_end_point = self.start_point + (self.radius*2*(i+1), self.radius*2+interval)
                else:
                    temp_end_point = self.start_point + (self.radius * 2 * (i + 1), -self.radius * 2 - interval)

                bend = DoubleBendConnector(temp_start_point, temp_end_point, width=self.width, z_start=self.z_start,
                                           z_end=self.z_end, material=self.material, rename=self.rename,
                                           radius=self.radius, direction=HORIZONTAL)

                temp_start_point = bend.get_end_point()

                self.bend_list.append(bend)

            temp_end_point = self.start_point + (self.radius*2*(self.segments+1), 0)
            bend = DoubleBendConnector(temp_start_point, temp_end_point, width=self.width, z_start=self.z_start,
                                           z_end=self.z_end, material=self.material, rename=self.rename,
                                           radius=self.radius, direction=HORIZONTAL)
            self.bend_list.append(bend)

            self.waveguide = Waveguide(temp_end_point, self.start_point + (self.distance, 0), width=self.width,
                                       z_start=self.z_start, z_end=self.z_end, material=self.material,
                                       rename=self.rename)

        elif self.waveguide_type == HORIZONTAL and self.start_point.x > self.end_point.x: # horizontal right to left condition
            for i in range(0, self.segments):
                if i%2 == 0:
                    temp_end_point = self.start_point + (-self.radius*2*(i+1), self.radius*2+interval)
                else:
                    temp_end_point = self.start_point + (-self.radius * 2 * (i + 1), -self.radius * 2 - interval)

                bend = DoubleBendConnector(temp_start_point, temp_end_point, width=self.width, z_start=self.z_start,
                                           z_end=self.z_end, material=self.material, rename=self.rename,
                                           radius=self.radius, direction=HORIZONTAL)

                temp_start_point = bend.get_end_point()

                self.bend_list.append(bend)

            temp_end_point = self.start_point + (-self.radius*2*(self.segments+1), 0)
            bend = DoubleBendConnector(temp_start_point, temp_end_point, width=self.width, z_start=self.z_start,
                                           z_end=self.z_end, material=self.material, rename=self.rename,
                                           radius=self.radius, direction=HORIZONTAL)
            self.bend_list.append(bend)

            self.waveguide = Waveguide(temp_end_point, self.start_point + (-self.distance, 0), width=self.width,
                                       z_start=self.z_start, z_end=self.z_end, material=self.material,
                                       rename=self.rename)

        elif self.waveguide_type == VERTICAL and self.start_point.y < self.end_point.y:# vertical lower to upper condition
            for i in range(0, self.segments):
                if i%2 == 0:
                    temp_end_point = self.start_point + (self.radius*2+interval, self.radius*2*(i+1))
                else:
                    temp_end_point = self.start_point + (-self.radius * 2 - interval, self.radius * 2 * (i + 1))

                bend = DoubleBendConnector(temp_start_point, temp_end_point, width=self.width, z_start=self.z_start,
                                           z_end=self.z_end, material=self.material, rename=self.rename,
                                           radius=self.radius, direction=VERTICAL)

                temp_start_point = bend.get_end_point()

                self.bend_list.append(bend)

            temp_end_point = self.start_point + (0, self.radius*2*(self.segments+1))
            bend = DoubleBendConnector(temp_start_point, temp_end_point, width=self.width, z_start=self.z_start,
                                           z_end=self.z_end, material=self.material, rename=self.rename,
                                           radius=self.radius, direction=VERTICAL)
            self.bend_list.append(bend)

            self.waveguide = Waveguide(temp_end_point, self.start_point + (0, self.distance), width=self.width,
                                       z_start=self.z_start, z_end=self.z_end, material=self.material,
                                       rename=self.rename)
        else: # vertical upper to lower condition
            for i in range(0, self.segments):
                if i%2 == 0:
                    temp_end_point = self.start_point + (self.radius*2+interval, -self.radius*2*(i+1))
                else:
                    temp_end_point = self.start_point + (-self.radius * 2 - interval, -self.radius * 2 * (i + 1))

                bend = DoubleBendConnector(temp_start_point, temp_end_point, width=self.width, z_start=self.z_start,
                                           z_end=self.z_end, material=self.material, rename=self.rename,
                                           radius=self.radius, direction=VERTICAL)

                temp_start_point = bend.get_end_point()

                self.bend_list.append(bend)

            temp_end_point = self.start_point + (0, -self.radius*2*(self.segments+1))
            bend = DoubleBendConnector(temp_start_point, temp_end_point, width=self.width, z_start=self.z_start,
                                           z_end=self.z_end, material=self.material, rename=self.rename,
                                           radius=self.radius, direction=VERTICAL)
            self.bend_list.append(bend)

            self.waveguide = Waveguide(temp_end_point, self.start_point + (0, -self.distance), width=self.width,
                                       z_start=self.z_start, z_end=self.z_end, material=self.material,
                                       rename=self.rename)


    def draw(self):
        bpy_obj_list = []
        for bend in self.bend_list:
            bpy_obj_list.append(bend.draw())

        bpy_obj_list.append(self.waveguide.draw())

        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy_obj_list:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = bpy_obj_list[-1]
        bpy.ops.object.join()
        wg = bpy.context.object
        return wg

    def get_start_point(self):
        """
        Derive the start point of the taper.

        Returns
        -------
        out : Point
            Start point.
        """
        return self.start_point

    def get_end_point(self):
        """
        Derive the end point of the taper.

        Returns
        -------
        out : Point
            End point.
        """
        return self.end_point