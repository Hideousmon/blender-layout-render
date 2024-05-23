from .utils import *
from .material import *
import bpy
import math
import bmesh

class Plane:
    def __init__(self, center_point, width = 1.0, height = 0.8, z_center = 0, normal_direction = HORIZONTAL, material=None, rename=None):
        center_point = tuple_to_point(center_point)
        self.center_point = center_point
        self.width = width
        self.height = height
        self.z_center = z_center
        self.material = material
        self.rename = rename
        self.location = (center_point.x, center_point.y, z_center)
        self.normal_direction = normal_direction


    def draw(self):
        bpy.ops.mesh.primitive_plane_add(size=1, location=self.location)
        bpy_object = bpy.context.active_object

        if self.normal_direction == HORIZONTAL:
            bpy_object.scale = (self.height, self.width, 1)
            bpy_object.rotation_euler = (0, math.pi/2, 0)
        else:
            bpy_object.scale = (self.width, self.height, 1)
            bpy_object.rotation_euler = (math.pi / 2, 0, 0)

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
            material.diffuse_color = self.material["Diffusion Color"]
        if not (self.rename == None):
            bpy_object.name = self.rename

        return bpy_object