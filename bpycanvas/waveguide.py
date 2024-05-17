from .utils import *

class Waveguide:
    def __init__(self):
        def __init__(self, start_point, end_point, width, z_start=None, z_end=None, material=None, rename=None):
            start_point = tuple_to_point(start_point)
            end_point = tuple_to_point(end_point)
            if start_point.x != end_point.x and start_point.y != end_point.y:
                raise Exception("Invalid Waveguide Parameter!")
            self.start_point = start_point
            self.end_point = end_point
            self.width = width
            self.z_start = z_start
            self.z_end = z_end
            self.material = material
            self.rename = rename
            if (start_point == end_point):
                self.ifexist = 0
            else:
                self.ifexist = 1
            if start_point.x == end_point.x:  # vertical waveguide
                self.down_left_x = start_point.x - width / 2
                self.down_left_y = start_point.y if (start_point.y < end_point.y) else end_point.y
                self.up_right_x = end_point.x + width / 2
                self.up_right_y = end_point.y if (start_point.y < end_point.y) else start_point.y
                self.waveguide_type = VERTICAL
            else:  # parallel waveguide
                self.down_left_x = start_point.x if (start_point.x < end_point.x) else end_point.x
                self.down_left_y = start_point.y - width / 2
                self.up_right_x = end_point.x if (start_point.x < end_point.x) else start_point.x
                self.up_right_y = end_point.y + width / 2
                self.waveguide_type = HORIZONTAL
