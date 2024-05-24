from .utils import *
from .polygon import Polygon
from .boolean import cut

class Grating:
    def __init__(self, start_point, z_start, z_end, relative_position = RIGHT, wg_width = 0.5, etch_depth = 0.07,
                 material = None, rename = None, scale = 1):
        self.start_point = tuple_to_point(start_point)
        self.z_start = z_start
        self.z_end = z_end
        self.relative_position = relative_position
        self.etch_depth = etch_depth
        self.material = material
        self.rename = rename

        self.etch_1_list = []
        self.etch_2_list = []
        self.etch_3_list = []
        self.etch_4_list = []
        self.etch_5_list = []
        self.etch_6_list = []
        self.poly_list = []

        # create poly_list
        self.poly_list.append(start_point + (0, wg_width / 2))
        self.poly_list.append(start_point + (0, wg_width / 2) + (10*scale, 10*scale))
        self.poly_list.append(start_point + (0, wg_width / 2) + (10*scale, 10*scale) + (20*scale, 0))
        self.poly_list.append(start_point + (0, -wg_width / 2) + (10*scale, -10*scale) + (20*scale, 0))
        self.poly_list.append(start_point + (0, -wg_width / 2) + (10*scale, -10*scale))
        self.poly_list.append(start_point + (0, -wg_width / 2))

        # create etch 1
        self.etch_1_list.append(start_point + (13*scale, 0) + (-0.5*scale, 10*scale + wg_width/2))
        self.etch_1_list.append(start_point + (13*scale, 0) + (0.5*scale, 10*scale + wg_width / 2))
        self.etch_1_list.append(start_point + (13*scale, 0) + (0.5*scale, -10*scale - wg_width / 2))
        self.etch_1_list.append(start_point + (13*scale, 0) + (-0.5*scale, -10*scale - wg_width/2))

        # create etch 2
        self.etch_2_list.append(start_point + (16*scale, 0) + (-0.5*scale, 10*scale + wg_width/2))
        self.etch_2_list.append(start_point + (16*scale, 0) + (0.5*scale, 10*scale + wg_width / 2))
        self.etch_2_list.append(start_point + (16*scale, 0) + (0.5*scale, -10*scale - wg_width / 2))
        self.etch_2_list.append(start_point + (16*scale, 0) + (-0.5*scale, -10*scale - wg_width/2))


        # create etch 3
        self.etch_3_list.append(start_point + (19*scale, 0) + (-0.5*scale, 10*scale + wg_width/2))
        self.etch_3_list.append(start_point + (19*scale, 0) + (0.5*scale, 10*scale + wg_width / 2))
        self.etch_3_list.append(start_point + (19*scale, 0) + (0.5*scale, -10*scale - wg_width / 2))
        self.etch_3_list.append(start_point + (19*scale, 0) + (-0.5*scale, -10*scale - wg_width/2))



        # create etch 4
        self.etch_4_list.append(start_point + (22*scale, 0) + (-0.5*scale, 10*scale + wg_width/2))
        self.etch_4_list.append(start_point + (22*scale, 0) + (0.5*scale, 10*scale + wg_width / 2))
        self.etch_4_list.append(start_point + (22*scale, 0) + (0.5*scale, -10*scale - wg_width / 2))
        self.etch_4_list.append(start_point + (22*scale, 0) + (-0.5*scale, -10*scale - wg_width/2))



        # create etch 5
        self.etch_5_list.append(start_point + (25*scale, 0) + (-0.5*scale, 10*scale + wg_width/2))
        self.etch_5_list.append(start_point + (25*scale, 0) + (0.5*scale, 10*scale + wg_width / 2))
        self.etch_5_list.append(start_point + (25*scale, 0) + (0.5*scale, -10*scale - wg_width / 2))
        self.etch_5_list.append(start_point + (25*scale, 0) + (-0.5*scale, -10*scale - wg_width/2))



        # create etch 6
        self.etch_6_list.append(start_point + (28*scale, 0) + (-0.5*scale, 10*scale + wg_width/2))
        self.etch_6_list.append(start_point + (28*scale, 0) + (0.5*scale, 10*scale + wg_width / 2))
        self.etch_6_list.append(start_point + (28*scale, 0) + (0.5*scale, -10*scale - wg_width / 2))
        self.etch_6_list.append(start_point + (28*scale, 0) + (-0.5*scale, -10*scale - wg_width/2))

        # rotation
        if self.relative_position == LEFT:
            theta = math.pi
        elif self.relative_position == UP:
            theta = math.pi / 2
        elif self.relative_position == DOWN:
            theta = math.pi * 3 / 2
        else: #RIGHT
            theta = 0

        for i in range(len(self.poly_list)):
            x = (self.poly_list[i].x - self.start_point.x) * math.cos(theta) - (self.poly_list[i].y - self.start_point.y) * math.sin(theta) + self.start_point.x
            y = (self.poly_list[i].x - self.start_point.x) * math.sin(theta) + (self.poly_list[i].y - self.start_point.y) * math.cos(theta) + self.start_point.y
            self.poly_list[i] = Point(x, y)

        for i in range(len(self.etch_1_list)):
            x = (self.etch_1_list[i].x - self.start_point.x) * math.cos(theta) - (self.etch_1_list[i].y - self.start_point.y) * math.sin(theta) + self.start_point.x
            y = (self.etch_1_list[i].x - self.start_point.x) * math.sin(theta) + (self.etch_1_list[i].y - self.start_point.y) * math.cos(theta) + self.start_point.y
            self.etch_1_list[i] = Point(x, y)

        for i in range(len(self.etch_2_list)):
            x = (self.etch_2_list[i].x - self.start_point.x) * math.cos(theta) - (self.etch_2_list[i].y - self.start_point.y) * math.sin(theta) + self.start_point.x
            y = (self.etch_2_list[i].x - self.start_point.x) * math.sin(theta) + (self.etch_2_list[i].y - self.start_point.y) * math.cos(theta) + self.start_point.y
            self.etch_2_list[i] = Point(x, y)

        for i in range(len(self.etch_3_list)):
            x = (self.etch_3_list[i].x - self.start_point.x) * math.cos(theta) - (self.etch_3_list[i].y - self.start_point.y) * math.sin(theta) + self.start_point.x
            y = (self.etch_3_list[i].x - self.start_point.x) * math.sin(theta) + (self.etch_3_list[i].y - self.start_point.y) * math.cos(theta) + self.start_point.y
            self.etch_3_list[i] = Point(x, y)

        for i in range(len(self.etch_4_list)):
            x = (self.etch_4_list[i].x - self.start_point.x) * math.cos(theta) - (self.etch_4_list[i].y - self.start_point.y) * math.sin(theta) + self.start_point.x
            y = (self.etch_4_list[i].x - self.start_point.x) * math.sin(theta) + (self.etch_4_list[i].y - self.start_point.y) * math.cos(theta) + self.start_point.y
            self.etch_4_list[i] = Point(x, y)

        for i in range(len(self.etch_5_list)):
            x = (self.etch_5_list[i].x - self.start_point.x) * math.cos(theta) - (self.etch_5_list[i].y - self.start_point.y) * math.sin(theta) + self.start_point.x
            y = (self.etch_5_list[i].x - self.start_point.x) * math.sin(theta) + (self.etch_5_list[i].y - self.start_point.y) * math.cos(theta) + self.start_point.y
            self.etch_5_list[i] = Point(x, y)

        for i in range(len(self.etch_6_list)):
            x = (self.etch_6_list[i].x - self.start_point.x) * math.cos(theta) - (self.etch_6_list[i].y - self.start_point.y) * math.sin(theta) + self.start_point.x
            y = (self.etch_6_list[i].x - self.start_point.x) * math.sin(theta) + (self.etch_6_list[i].y - self.start_point.y) * math.cos(theta) + self.start_point.y
            self.etch_6_list[i] = Point(x, y)

        self.base_poly = Polygon(self.poly_list, self.z_start, self.z_end, material=self.material)
        self.etch_poly1 = Polygon(self.etch_1_list, self.z_end - self.etch_depth, self.z_end)
        self.etch_poly2 = Polygon(self.etch_2_list, self.z_end - self.etch_depth, self.z_end)
        self.etch_poly3 = Polygon(self.etch_3_list, self.z_end - self.etch_depth, self.z_end)
        self.etch_poly4 = Polygon(self.etch_4_list, self.z_end - self.etch_depth, self.z_end)
        self.etch_poly5 = Polygon(self.etch_5_list, self.z_end - self.etch_depth, self.z_end)
        self.etch_poly6 = Polygon(self.etch_6_list, self.z_end - self.etch_depth, self.z_end)

    def draw(self):
        base_obj = self.base_poly.draw()
        etch_obj1 = self.etch_poly1.draw()
        etch_obj2 = self.etch_poly2.draw()
        etch_obj3 = self.etch_poly3.draw()
        etch_obj4 = self.etch_poly4.draw()
        etch_obj5 = self.etch_poly5.draw()
        etch_obj6 = self.etch_poly6.draw()
        bpy.ops.object.select_all(action='DESELECT')
        etch_obj1.select_set(True)
        etch_obj2.select_set(True)
        etch_obj3.select_set(True)
        etch_obj4.select_set(True)
        etch_obj5.select_set(True)
        etch_obj6.select_set(True)
        bpy.context.view_layer.objects.active = etch_obj1
        bpy.ops.object.join()
        etch_obj = bpy.context.object
        cut(base_obj, etch_obj)
        return base_obj

    def get_start_point(self):
        return self.start_point