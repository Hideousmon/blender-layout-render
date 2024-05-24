from .utils import *
from .polygon import *
import bpy

class Bend:
    def __init__(self,center_point, start_radian, end_radian, width, radius, z_start, z_end, material = None, rename = None):
        self.center_point = tuple_to_point(center_point)
        self.start_radian = start_radian
        self.end_radian = end_radian
        self.width = width
        self.radius = radius
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename
        self.start_point = Point(self.center_point.x + radius*math.cos(start_radian),
                                 self.center_point.y + radius*math.sin(start_radian))
        self.end_point = Point(self.center_point.x + radius * math.cos(end_radian),
                                 self.center_point.y + radius * math.sin(end_radian))

    def draw(self, segments = 100):
        # inside
        inside_points_list = []
        for i in range(segments + 1):
            angle = self.start_radian + (self.end_radian - self.start_radian) * (i / segments)
            x = (self.radius - self.width/2) * math.cos(angle)
            y = (self.radius - self.width / 2) * math.sin(angle)
            inside_points_list.append(Point(x, y))
        # outside
        outside_points_list = []
        for i in range(segments + 1):
            angle = self.end_radian - (self.end_radian - self.start_radian) * (i / segments)
            x = (self.radius + self.width / 2) * math.cos(angle)
            y = (self.radius + self.width / 2) * math.sin(angle)
            outside_points_list.append(Point(x, y))

        points_list = inside_points_list + outside_points_list
        poly = Polygon(points_list, self.z_start, self.z_end, material=self.material, rename=self.rename)
        poly_obj = poly.draw()

        return poly_obj

    def get_start_point(self):
        return  self.start_point

    def get_end_point(self):
        return  self.end_point