from .utils import *
from .quarbend import AQuarBend,QuarBend

class DoubleBendConnector:
    def __init__(self,start_point,end_point,width, z_start, z_end, material = None, rename = None, radius=5, xpercent = 0.5 , ypercent = 0.5,direction =  HORIZONTAL):
        self.start_point = tuple_to_point(start_point)
        self.end_point = tuple_to_point(end_point)
        self.radius = radius
        self.width = width
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename
        self.x_percent = xpercent
        self.y_percent = ypercent
        self.direction = direction
        self.center_point = Point(self.start_point.x + (self.end_point.x - self.start_point.x)*self.x_percent, self.start_point.y + (self.end_point.y - self.start_point.y)*self.y_percent)

        if (math.fabs(self.start_point.x - self.center_point.x) < self.radius or math.fabs(self.start_point.y - self.center_point.y) < self.radius
        or math.fabs(self.end_point.x - self.center_point.x) < self.radius or math.fabs(self.end_point.y - self.center_point.y) < self.radius):
            raise Exception("Two Points are too Near to Use DoubleBendConnector Or the Percent Need to be Adjusted!")

        if (self.start_point.x < self.end_point.x and self.start_point.y < self.end_point.y): ## up right type
            if (self.direction == HORIZONTAL):
                self.first_bend = AQuarBend(self.start_point, self.center_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
                self.second_bend = QuarBend(self.center_point, self.end_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
            elif (self.direction == VERTICAL):
                self.first_bend = QuarBend(self.start_point, self.center_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
                self.second_bend = AQuarBend(self.center_point, self.end_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
            else:
                raise  Exception("Wrong direction expression!")
        elif (self.start_point.x < self.end_point.x and self.start_point.y > self.end_point.y): ## down right type
            if (self.direction == HORIZONTAL):
                self.first_bend = QuarBend(self.start_point, self.center_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
                self.second_bend = AQuarBend(self.center_point, self.end_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
            elif (self.direction == VERTICAL):
                self.first_bend = AQuarBend(self.start_point, self.center_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
                self.second_bend = QuarBend(self.center_point, self.end_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
            else:
                raise Exception("Wrong direction expression!")
        elif (self.start_point.x > self.end_point.x and self.start_point.y > self.end_point.y): ## down left type
            if (self.direction == HORIZONTAL):
                self.first_bend = AQuarBend(self.start_point, self.center_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
                self.second_bend = QuarBend(self.center_point, self.end_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
            elif (self.direction == VERTICAL):
                self.first_bend = QuarBend(self.start_point, self.center_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
                self.second_bend = AQuarBend(self.center_point, self.end_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
            else:
                raise Exception("Wrong direction expression!")
        elif (self.start_point.x > self.end_point.x and self.start_point.y < self.end_point.y): ## up left type
            if (self.direction == HORIZONTAL):
                self.first_bend = QuarBend(self.start_point, self.center_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
                self.second_bend = AQuarBend(self.center_point, self.end_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
            elif (self.direction == VERTICAL):
                self.first_bend = AQuarBend(self.start_point, self.center_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
                self.second_bend = QuarBend(self.center_point, self.end_point, width, radius = self.radius, z_start = self.z_start, z_end = self.z_end, material = self.material, rename = self.rename)
            else:
                raise Exception("Wrong direction expression!")
        else:
            raise Exception("Unexpected DoubleBendConnector Error!")

    def draw(self):
        bend_obj_1 = self.first_bend.draw()
        bend_obj_2 = self.second_bend.draw()
        bpy.ops.object.select_all(action='DESELECT')
        bend_obj_1.select_set(True)
        bend_obj_2.select_set(True)
        bpy.context.view_layer.objects.active = bend_obj_1
        bpy.ops.object.join()
        dc = bpy.context.object
        return dc

    def get_start_point(self):
        return  self.start_point

    def get_end_point(self):
        return  self.end_point