from .utils import *
from .material import *
import bpy

class Ribbon:
    def __init__(self, point3d_list, width, thickness = 0.1, rotation_degree = 90, material=None, rename=None):
        self.point_list = point3d_list
        self.width = width
        self.thickness = thickness
        self.rotation_degree = rotation_degree
        self.material = material
        self.rename = rename

    def draw(self):
        curve_data = bpy.data.curves.new(name='RibbonCurve', type='CURVE')
        curve_data.dimensions = '3D'

        spline = curve_data.splines.new(type='BEZIER')
        spline.bezier_points.add(len(self.point_list) - 1)

        for i, point in enumerate(self.point_list):
            spline.bezier_points[i].co = point

        for point in spline.bezier_points:
            point.tilt = math.radians(self.rotation_degree)

        for point in spline.bezier_points:
            point.handle_left_type = 'AUTO'
            point.handle_right_type = 'AUTO'

        curve_data.bevel_depth = self.thickness
        curve_data.bevel_resolution = 1

        curve_data.fill_mode = 'FULL'
        curve_data.extrude = self.width

        bpy_object = bpy.data.objects.new('RibbonCurve', curve_data)
        bpy.context.collection.objects.link(bpy_object)

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
