from .utils import *
from .bend import Bend

class SBend:
    def __init__(self,start_point, end_point, width, z_start, z_end, length=None,radius=5, material = None, rename = None):
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename
        if (length != None and radius != None): # overwrite the properties of S-Bend
            self.start_point = tuple_to_point(start_point)
            self.length = length
            self.radius = radius
            self.width = width
            self.radian = self.length/2/self.radius
            if (self.start_point.x > end_point.x and self.start_point.y > end_point.y): ## left down type
                self.delta_y = self.radius * math.sin(self.radian) * 2
                self.delta_x = (self.radius - self.radius * math.cos(self.radian)) * 2
                self.end_point = self.start_point + (-self.delta_x,-self.delta_y)
            if (self.start_point.x < end_point.x and self.start_point.y > end_point.y):  ## right down type
                self.delta_x = self.radius * math.sin(self.radian) * 2
                self.delta_y = (self.radius - self.radius * math.cos(self.radian)) * 2
                self.end_point = self.start_point + (self.delta_x, -self.delta_y)
            if (self.start_point.x < end_point.x and self.start_point.y < end_point.y):  ## right up type
                self.delta_y = self.radius * math.sin(self.radian) * 2
                self.delta_x = (self.radius - self.radius * math.cos(self.radian)) * 2
                self.end_point = self.start_point + (self.delta_x, self.delta_y)
            if (self.start_point.x > end_point.x and self.start_point.y < end_point.y):  ## left up type
                self.delta_x = self.radius * math.sin(self.radian) * 2
                self.delta_y = (self.radius - self.radius * math.cos(self.radian)) * 2
                self.end_point = self.start_point + (-self.delta_x, self.delta_y)

        else:
            self.start_point = tuple_to_point(start_point)
            self.end_point = tuple_to_point(end_point)
            self.width = width

            ## calculate radius and radian
            self.delta_x = abs(self.start_point.x - end_point.x)
            self.delta_y = abs(self.start_point.y - end_point.y)

            if (self.start_point.x > end_point.x and self.start_point.y > end_point.y) or (self.start_point.x < end_point.x and self.start_point.y < end_point.y):
                self.theta = math.atan(self.delta_y / self.delta_x)
            else:
                self.theta = math.atan(self.delta_x / self.delta_y)
            self.radian = math.pi - 2 * self.theta
            self.radius = math.sin(self.theta) * math.sqrt(
                math.pow(self.delta_x / 2, 2) + math.pow(self.delta_y / 2, 2)) / math.sin(self.radian)
            if (self.radius < 5):
                print("Warning! The radius of the bends in SBend is too small! The radius now is:" + str(
                    self.radius) + "μm.")
            self.length = self.radian * self.radius

        ## identify the type of S-Bend
        if (self.start_point.x > end_point.x and self.start_point.y > end_point.y): ## left down type
            self.first_bend_center_point = self.start_point + (-self.radius,0)
            self.first_bend = Bend(self.first_bend_center_point,-self.radian,0,self.width,self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_bend_center_point = self.end_point + (self.radius,0)
            self.second_bend = Bend(self.second_bend_center_point,math.pi - self.radian, math.pi,self.width,self.radius, self.z_start, self.z_end, self.material, self.rename)

        if (self.start_point.x < end_point.x and self.start_point.y > end_point.y): ## right down type
            self.first_bend_center_point = self.start_point + (0, -self.radius)
            self.first_bend = Bend(self.first_bend_center_point, math.pi/2 - self.radian, math.pi/2, self.width, self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_bend_center_point = self.end_point + (0, self.radius)
            self.second_bend = Bend(self.second_bend_center_point, math.pi*3/2 - self.radian, math.pi*3/2, self.width,
                                    self.radius, self.z_start, self.z_end, self.material, self.rename)

        if (self.start_point.x < end_point.x and self.start_point.y < end_point.y):  ## right up type
            self.first_bend_center_point = self.start_point + (self.radius, 0)
            self.first_bend = Bend(self.first_bend_center_point, math.pi - self.radian, math.pi, self.width, self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_bend_center_point = self.end_point + (-self.radius, 0)
            self.second_bend = Bend(self.second_bend_center_point, - self.radian, 0, self.width,
                                    self.radius, self.z_start, self.z_end, self.material, self.rename)

        if (self.start_point.x > end_point.x and self.start_point.y < end_point.y): ## left up type
            self.first_bend_center_point = self.start_point + (0, self.radius)
            self.first_bend = Bend(self.first_bend_center_point, math.pi*3 / 2 - self.radian, math.pi*3 / 2, self.width,
                                   self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_bend_center_point = self.end_point + (0, -self.radius)
            self.second_bend = Bend(self.second_bend_center_point, math.pi / 2 - self.radian, math.pi / 2,
                                    self.width,
                                    self.radius, self.z_start, self.z_end, self.material, self.rename)

    def draw(self):
        bend_obj_1 = self.first_bend.draw()
        bend_obj_2 = self.second_bend.draw()
        bpy.ops.object.select_all(action='DESELECT')
        bend_obj_1.select_set(True)
        bend_obj_2.select_set(True)
        bpy.context.view_layer.objects.active = bend_obj_1
        bpy.ops.object.join()
        s_bend = bpy.context.object
        return s_bend

    def get_start_point(self):
        return self.start_point

    def get_end_point(self):
        return self.end_point

    def get_length(self):
        return self.length


class ASBend:
    def __init__(self, start_point, end_point, width, z_start, z_end, length=None, radius=5, material = None, rename = None):
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename
        if (length != None and radius != None):  # overwrite the properties of S-Bend
            self.start_point = tuple_to_point(start_point)
            self.length = length
            self.radius = radius
            self.width = width
            self.radian = self.length / 2 / self.radius

            if (self.start_point.x > end_point.x and self.start_point.y > end_point.y):  ## left down type
                self.delta_x = self.radius * math.sin(self.radian) * 2
                self.delta_y = (self.radius - self.radius * math.cos(self.radian)) * 2
                self.end_point = self.start_point + (-self.delta_x, -self.delta_y)
            if (self.start_point.x < end_point.x and self.start_point.y > end_point.y):  ## right down type
                self.delta_y = self.radius * math.sin(self.radian) * 2
                self.delta_x = (self.radius - self.radius * math.cos(self.radian)) * 2
                self.end_point = self.start_point + (self.delta_x, -self.delta_y)
            if (self.start_point.x < end_point.x and self.start_point.y < end_point.y):  ## right up type
                self.delta_x = self.radius * math.sin(self.radian) * 2
                self.delta_y = (self.radius - self.radius * math.cos(self.radian)) * 2
                self.end_point = self.start_point + (self.delta_x, self.delta_y)
            if (self.start_point.x > end_point.x and self.start_point.y < end_point.y):  ## left up type
                self.delta_y = self.radius * math.sin(self.radian) * 2
                self.delta_x = (self.radius - self.radius * math.cos(self.radian)) * 2
                self.end_point = self.start_point + (-self.delta_x, self.delta_y)

        else:
            self.start_point = tuple_to_point(start_point)
            self.end_point = tuple_to_point(end_point)
            self.width = width

            ## calculate radius and radian
            self.delta_x = abs(self.start_point.x - end_point.x)
            self.delta_y = abs(self.start_point.y - end_point.y)

            if (self.start_point.x < end_point.x and self.start_point.y > end_point.y) or (
                    self.start_point.x > end_point.x and self.start_point.y < end_point.y):
                self.theta = math.atan(self.delta_y / self.delta_x)
            else:
                self.theta = math.atan(self.delta_x / self.delta_y)
            self.radian = math.pi - 2 * self.theta
            self.radius = math.sin(self.theta) * math.sqrt(
                math.pow(self.delta_x / 2, 2) + math.pow(self.delta_y / 2, 2)) / math.sin(self.radian)
            if (self.radius < 5):
                print("Warning! The radius of the bends in SBend is too small! The radius now is:" + str(
                    self.radius) + "μm.")
            self.length = self.radian * self.radius

        ## identify the type of S-Bend
        if (self.start_point.x > end_point.x and self.start_point.y > end_point.y): ## left down type
            self.first_bend_center_point = self.start_point + (0,-self.radius)
            self.first_bend = Bend(self.first_bend_center_point,math.pi/2,math.pi/2 + self.radian,self.width,self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_bend_center_point = self.end_point + (0,self.radius)
            self.second_bend = Bend(self.second_bend_center_point,math.pi*3/2 , math.pi*3/2 + self.radian,self.width,self.radius, self.z_start, self.z_end, self.material, self.rename)

        if (self.start_point.x < end_point.x and self.start_point.y > end_point.y): ## right down type
            self.first_bend_center_point = self.start_point + (self.radius, 0)
            self.first_bend = Bend(self.first_bend_center_point, math.pi , math.pi + self.radian, self.width,
                                   self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_bend_center_point = self.end_point + (-self.radius, 0)
            self.second_bend = Bend(self.second_bend_center_point,0,  self.radian,
                                    self.width, self.radius, self.z_start, self.z_end, self.material, self.rename)

        if (self.start_point.x < end_point.x and self.start_point.y < end_point.y):  ## right up type
            self.first_bend_center_point = self.start_point + (0, self.radius)
            self.first_bend = Bend(self.first_bend_center_point, math.pi*3 / 2, math.pi*3 / 2 + self.radian, self.width,
                                   self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_bend_center_point = self.end_point + (0, -self.radius)
            self.second_bend = Bend(self.second_bend_center_point, math.pi / 2, math.pi / 2 + self.radian,
                                    self.width, self.radius, self.z_start, self.z_end, self.material, self.rename)

        if (self.start_point.x > end_point.x and self.start_point.y < end_point.y): ## left up type
            self.first_bend_center_point = self.start_point + (-self.radius, 0)
            self.first_bend = Bend(self.first_bend_center_point, 0 ,  self.radian, self.width,
                                   self.radius, self.z_start, self.z_end, self.material, self.rename)
            self.second_bend_center_point = self.end_point + (self.radius, 0)
            self.second_bend = Bend(self.second_bend_center_point, math.pi,  math.pi + self.radian,
                                    self.width, self.radius, self.z_start, self.z_end, self.material, self.rename)

    def draw(self):
        bend_obj_1 = self.first_bend.draw()
        bend_obj_2 = self.second_bend.draw()
        bpy.ops.object.select_all(action='DESELECT')
        bend_obj_1.select_set(True)
        bend_obj_2.select_set(True)
        bpy.context.view_layer.objects.active = bend_obj_1
        bpy.ops.object.join()
        s_bend = bpy.context.object
        return s_bend

    def get_start_point(self):
        return self.start_point

    def get_end_point(self):
        return self.end_point

    def get_length(self):
        return self.length

