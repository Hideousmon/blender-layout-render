from .utils import *
from .material import *
import bpy

class Waveguide:
    def __init__(self, start_point, end_point, width, z_start, z_end, material=None, rename=None):
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
            self.location = (start_point.x, (start_point.y + end_point.y)/2, (z_start + z_end) / 2)
            self.scale = (width, abs(start_point.y - end_point.y), abs(z_end - z_start))
            self.waveguide_type = VERTICAL
        else:  # horizontal waveguide
            self.location = ((start_point.x + end_point.x) / 2, start_point.y, (z_start + z_end) / 2)
            self.scale = (abs(start_point.x - end_point.x), width, abs(z_end - z_start))
            self.waveguide_type = HORIZONTAL

    def draw(self):
        bpy.ops.mesh.primitive_cube_add(size=1, location=self.location)
        bpy_object = bpy.context.active_object
        bpy_object.scale = self.scale
        if not (self.material == None):
            material = bpy.data.materials.new(name=self.material["Name"])
            material.use_nodes = True
            mat_nodes = material.node_tree.nodes
            mat_links = material.node_tree.links
            bpy_object.data.materials.append(material)

            mat_nodes["Principled BSDF"].inputs["Metallic"].default_value = self.material["Metallic"]
            mat_nodes["Principled BSDF"].inputs["Base Color"].default_value = self.material["Base Color"]
            mat_nodes["Principled BSDF"].inputs["Roughness"].default_value = self.material["Roughness"]
            mat_nodes["Principled BSDF"].inputs["IOR"].default_value = self.material["IOR"]
            mat_nodes["Principled BSDF"].inputs["Alpha"].default_value = self.material["Alpha"]
        if not (self.rename == None):
            bpy_object.name = self.rename

        return bpy_object