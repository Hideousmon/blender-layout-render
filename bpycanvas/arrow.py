from .utils import *
from .material import *
import bpy
import numpy as np
import math
import mathutils

class Arrow:
    def __init__(self, start_point, end_point, width, z_start = 0, z_end = 0, material=None, rename=None):
        start_point = tuple_to_point(start_point)
        end_point = tuple_to_point(end_point)
        self.start_point = start_point
        self.end_point = end_point
        self.width = width
        self.material = material
        self.rename = rename
        if (start_point == end_point):
            self.ifexist = 0
        else:
            self.ifexist = 1

        self.location_shaft = ((start_point.x + end_point.y)/2, (start_point.y + end_point.y)/2, (z_start + z_end) / 2)
        self.radius_shaft = width/2
        self.radius_head = self.radius_shaft * 3
        self.depth_head = self.radius_head/3 * 10


        vector = np.array([end_point.x - start_point.x, end_point.y - start_point.y, z_end - z_start])
        direction = mathutils.Vector(vector)
        length = direction.length
        self.depth_shaft = length
        self.location_head = np.array([(start_point.x + end_point.y)/2, (start_point.y + end_point.y)/2,
                                       (z_start + z_end) / 2]) + vector*(
                self.depth_shaft/2 + self.depth_head/2) / length

        direction.normalize()
        up_vector = mathutils.Vector((0, 0, -1))
        self.rotation = direction.rotation_difference(up_vector).to_euler()
        print(vector)
        print(direction)
        print(self.rotation)


    def draw(self):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=self.radius_shaft,
            depth=self.depth_shaft,
            location=self.location_shaft
        )
        arrow_shaft = bpy.context.object
        arrow_shaft.rotation_euler = self.rotation

        bpy.ops.mesh.primitive_cone_add(
            radius1=self.radius_head,
            depth=self.depth_head,
            location=self.location_head
        )
        arrow_head = bpy.context.object
        arrow_head.rotation_euler = self.rotation

        bpy.ops.object.select_all(action='DESELECT')
        arrow_shaft.select_set(True)
        arrow_head.select_set(True)
        bpy.context.view_layer.objects.active = arrow_shaft
        bpy.ops.object.join()
        arrow = bpy.context.object

        if not (self.material == None):
            material = bpy.data.materials.new(name=self.material["Name"])
            material.use_nodes = True
            mat_nodes = material.node_tree.nodes
            mat_links = material.node_tree.links
            arrow_shaft.data.materials.append(material)

            mat_nodes["Principled BSDF"].inputs["Metallic"].default_value = self.material["Metallic"]
            mat_nodes["Principled BSDF"].inputs["Base Color"].default_value = self.material["Base Color"]
            mat_nodes["Principled BSDF"].inputs["Roughness"].default_value = self.material["Roughness"]
            mat_nodes["Principled BSDF"].inputs["IOR"].default_value = self.material["IOR"]
            mat_nodes["Principled BSDF"].inputs["Alpha"].default_value = self.material["Alpha"]
            material.diffuse_color = self.material["Diffusion Color"]
        if not (self.rename == None):
            arrow.name = self.rename
        else:
            arrow.name = "Arrow"

        return arrow