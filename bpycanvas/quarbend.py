from .utils import *
from .waveguide import Waveguide
from .bend import Bend

# anticlockwise
class AQuarBend:
    def __init__(self,start_point,end_point,width, z_start, z_end, radius=5, material = None, rename = None):
        self.start_point = tuple_to_point(start_point)
        self.end_point = tuple_to_point(end_point)
        self.radius = radius
        self.width = width
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename

        if (self.start_point.x < self.end_point.x and self.start_point.y > self.end_point.y): ## left down type
            if (self.end_point.x - self.start_point.x < self.radius) or (self.start_point.y - self.end_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(self.start_point,Point(self.start_point.x,self.end_point.y + self.radius),self.width, self.z_start, self.z_end, self.material, self.rename)
            self.center_bend = Bend(Point(self.start_point.x + self.radius, self.end_point.y + self.radius), math.pi, math.pi*3/2, self.width , self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_waveguide = Waveguide(Point(self.start_point.x + self.radius,self.end_point.y),self.end_point ,self.width, self.z_start, self.z_end, self.material, self.rename)

        if (self.start_point.x < self.end_point.x and self.start_point.y < self.end_point.y): ## right down type
            if (self.end_point.x - self.start_point.x < self.radius) or (self.end_point.y - self.start_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(self.start_point,Point(self.end_point.x - self.radius,self.start_point.y),self.width, self.z_start, self.z_end, self.material, self.rename)
            self.center_bend = Bend(Point(self.end_point.x - self.radius, self.start_point.y + self.radius), -math.pi/2, 0 , self.width , self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_waveguide = Waveguide(Point(self.end_point.x,self.start_point.y + self.radius),self.end_point ,self.width, self.z_start, self.z_end, self.material, self.rename)

        if (self.start_point.x > self.end_point.x and self.start_point.y < self.end_point.y):  ## right up type
            if (self.start_point.x - self.end_point.x < self.radius) or (
                    self.end_point.y - self.start_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(self.start_point, Point(self.start_point.x, self.end_point.y - self.radius), self.width, self.z_start, self.z_end, self.material, self.rename)
            self.center_bend = Bend(Point(self.start_point.x - self.radius, self.end_point.y - self.radius), 0 , math.pi / 2,
                                    self.width, self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_waveguide = Waveguide(Point(self.start_point.x - self.radius, self.end_point.y), self.end_point, self.width, self.z_start, self.z_end, self.material, self.rename)


        if (self.start_point.x > self.end_point.x and self.start_point.y > self.end_point.y): ## left up type
            if (self.start_point.x - self.end_point.x < self.radius) or (self.start_point.y - self.end_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(self.start_point,Point(self.end_point.x + self.radius,self.start_point.y),self.width, self.z_start, self.z_end, self.material, self.rename)
            self.center_bend = Bend(Point(self.end_point.x + self.radius, self.start_point.y - self.radius), math.pi/2, math.pi, self.width , self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_waveguide = Waveguide(Point(self.end_point.x,self.start_point.y - self.radius),self.end_point ,self.width, self.z_start, self.z_end, self.material, self.rename)

    def draw(self):
        wg_obj_1 = self.first_waveguide.draw()
        bend_obj_1 = self.center_bend.draw()
        wg_obj_2 = self.second_waveguide.draw()
        bpy.ops.object.select_all(action='DESELECT')
        wg_obj_1.select_set(True)
        bend_obj_1.select_set(True)
        wg_obj_2.select_set(True)
        bpy.context.view_layer.objects.active = bend_obj_1
        bpy.ops.object.join()
        quar_bend = bpy.context.object

        return quar_bend

    def get_start_point(self):
        return  self.start_point

    def get_end_point(self):
        return  self.end_point


class QuarBend:
    def __init__(self,start_point,end_point,width, z_start, z_end,radius=5, material = None, rename = None):
        self.start_point = tuple_to_point(start_point)
        self.end_point = tuple_to_point(end_point)
        self.radius = radius
        self.width = width
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename

        if (self.start_point.x < self.end_point.x and self.start_point.y > self.end_point.y): ## right up type
            if (self.end_point.x - self.start_point.x < self.radius) or (self.start_point.y - self.end_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(self.start_point,Point(self.end_point.x - self.radius,self.start_point.y),self.width, self.z_start, self.z_end, self.material, self.rename)
            self.center_bend = Bend(Point(self.end_point.x - self.radius, self.start_point.y - self.radius), 0, math.pi/2, self.width , self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_waveguide = Waveguide(Point(self.end_point.x,self.start_point.y - self.radius),self.end_point ,self.width, self.z_start, self.z_end, self.material, self.rename)

        if (self.start_point.x < self.end_point.x and self.start_point.y < self.end_point.y): ## left up type
            if (self.end_point.x - self.start_point.x < self.radius) or (self.end_point.y - self.start_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(self.start_point,Point(self.start_point.x,self.end_point.y - self.radius),self.width, self.z_start, self.z_end, self.material, self.rename)
            self.center_bend = Bend(Point(self.start_point.x + self.radius, self.end_point.y - self.radius), math.pi/2, math.pi , self.width , self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_waveguide = Waveguide(Point(self.start_point.x + self.radius,self.end_point.y),self.end_point ,self.width, self.z_start, self.z_end, self.material, self.rename)

        if (self.start_point.x > self.end_point.x and self.start_point.y < self.end_point.y):  ## down left type
            if (self.start_point.x - self.end_point.x < self.radius) or (
                    self.end_point.y - self.start_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(self.start_point, Point(self.end_point.x + self.radius, self.start_point.y), self.width, self.z_start, self.z_end, self.material, self.rename)
            self.center_bend = Bend(Point(self.end_point.x + self.radius, self.start_point.y + self.radius), math.pi , math.pi*3 / 2,
                                    self.width, self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_waveguide = Waveguide(Point(self.end_point.x, self.start_point.y + self.radius), self.end_point, self.width, self.z_start, self.z_end, self.material, self.rename)


        if (self.start_point.x > self.end_point.x and self.start_point.y > self.end_point.y): ## right down type
            if (self.start_point.x - self.end_point.x < self.radius) or (self.start_point.y - self.end_point.y < self.radius):
                raise Exception("Distance between two point is too short!")
            self.first_waveguide = Waveguide(self.start_point,Point(self.start_point.x,self.end_point.y + self.radius),self.width, self.z_start, self.z_end, self.material, self.rename)
            self.center_bend = Bend(Point(self.start_point.x - self.radius, self.end_point.y + self.radius),  - math.pi/2, 0 , self.width , self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_waveguide = Waveguide(Point(self.start_point.x - self.radius,self.end_point.y),self.end_point ,self.width, self.z_start, self.z_end, self.material, self.rename)

    def draw(self):
        wg_obj_1 = self.first_waveguide.draw()
        bend_obj_1 = self.center_bend.draw()
        wg_obj_2 = self.second_waveguide.draw()
        bpy.ops.object.select_all(action='DESELECT')
        wg_obj_1.select_set(True)
        bend_obj_1.select_set(True)
        wg_obj_2.select_set(True)
        bpy.context.view_layer.objects.active = bend_obj_1
        bpy.ops.object.join()
        quar_bend = bpy.context.object

        return quar_bend

    def get_start_point(self):
        return  self.start_point

    def get_end_point(self):
        return  self.end_point