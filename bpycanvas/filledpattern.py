from .utils import *
from .material import *
import bpy

class Circle:
    def __init__(self, center_point, radius, z_start, z_end, material = None, rename = None, vertices = 32):
        self.center_point = tuple_to_point(center_point)
        self.radius = radius
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename
        self.vertices = vertices

    def draw(self):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=self.radius,
            depth=abs(self.z_end-self.z_start),
            location=(self.center_point.x, self.center_point.y, (self.z_start + self.z_end)/2),
            vertices=self.vertices
        )
        bpy_object = bpy.context.active_object

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


    def get_center_point(self):
        return self.center_point


class Rectangle:
    def __init__(self, center_point, width, z_start, z_end, height = None, material = None, rename = None):
        self.center_point = tuple_to_point(center_point)
        self.width = width
        if height is None:
            self.height = width
        else:
            self.height = height

        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename
        self.location = (center_point.x, center_point.y, (z_start + z_end) / 2)
        self.scale = (self.width, self.height, abs(z_end - z_start))

    def draw(self):
        bpy.ops.mesh.primitive_cube_add(size=1, location=self.location)
        bpy_object = bpy.context.active_object
        bpy_object.scale = self.scale
        if not self.material is None:
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
        if not self.rename is None:
            bpy_object.name = self.rename

        return bpy_object

    def get_center_point(self):

        return self.center_point
