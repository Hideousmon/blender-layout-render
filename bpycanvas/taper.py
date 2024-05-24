from .utils import *
from .polygon import Polygon

class Taper():
    def __init__(self, start_point, end_point, start_width, end_width, z_start, z_end , material = None, rename = None):
        self.start_point = tuple_to_point(start_point)
        self.end_point = tuple_to_point(end_point)
        if start_point.x != end_point.x and start_point.y != end_point.y:
            raise Exception("Invalid Taper Parameter!")
        self.start_width = start_width
        self.end_width = end_width
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename
        if (start_point == end_point):
            self.ifexist = 0
        else:
            self.ifexist = 1
        if start_point.x == end_point.x:  ## vertical taper
            # if (math.fabs(start_point.y - end_point.y) < 5):
            #     raise Exception("Taper Too Short!")
            self.down_left_x = start_point.x - start_width / 2 if (start_point.y < end_point.y) else start_point.x - end_width / 2
            self.down_left_y = start_point.y if (start_point.y < end_point.y) else end_point.y
            self.down_right_x = start_point.x + start_width / 2 if (start_point.y < end_point.y) else start_point.x + end_width / 2
            self.down_right_y = start_point.y if (start_point.y < end_point.y) else end_point.y
            self.up_right_x = end_point.x + end_width / 2 if (start_point.y < end_point.y) else start_point.x + start_width / 2
            self.up_right_y = end_point.y if (start_point.y < end_point.y) else start_point.y
            self.up_left_x = end_point.x - end_width / 2 if (start_point.y < end_point.y) else start_point.x - start_width / 2
            self.up_left_y = end_point.y if (start_point.y < end_point.y) else start_point.y
            self.taper_type = VERTICAL
        else:  ## parallel waveguide
            # if (math.fabs(start_point.x - end_point.x) < 5):
            #     raise Exception("Taper Too Short!")
            self.down_left_x = start_point.x if (start_point.x < end_point.x) else end_point.x
            self.down_left_y = start_point.y - start_width / 2 if (start_point.x < end_point.x) else end_point.y - end_width / 2
            self.down_right_x = end_point.x if (start_point.x < end_point.x) else start_point.x
            self.down_right_y = end_point.y - end_width / 2  if (start_point.x < end_point.x) else start_point.y - start_width / 2
            self.up_right_x = end_point.x if (start_point.x < end_point.x) else start_point.x
            self.up_right_y = end_point.y + end_width / 2 if (start_point.x < end_point.x) else start_point.y + start_width / 2
            self.up_left_x = start_point.x if (start_point.x < end_point.x) else end_point.x
            self.up_left_y = start_point.y + start_width / 2 if (start_point.x < end_point.x) else end_point.y + end_width / 2
            self.taper_type =  HORIZONTAL

    def draw(self):
        taper_pts = [(self.down_left_x,self.down_left_y),(self.down_right_x,self.down_right_y),
                     (self.up_right_x,self.up_right_y),(self.up_left_x,self.up_left_y)]
        if self.ifexist:
            taper = Polygon(taper_pts, self.z_start, self.z_end, self.material, self.rename)
            taper_obj = taper.draw()
            return taper_obj
        else:
            return None

    def get_start_point(self):
        return self.start_point

    def get_end_point(self):
        return self.end_point