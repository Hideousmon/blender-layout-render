import bpy
import math
from bpycanvas import *

class LinesFlow:
    def __init__(self, point3d_list, width, material1=None, material2=None, rename=None, rotation_degree = 90,
                 emission_strength = 10):
        self.point_list = point3d_list
        self.width = width
        self.material1 = material1
        self.material2 = material2
        self.rename = rename
        self.rotation_degree = rotation_degree
        self.emission_strength = emission_strength

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

        curve_data.bevel_resolution = 1

        curve_data.fill_mode = 'FULL'
        curve_data.extrude = self.width

        bpy_object = bpy.data.objects.new('RibbonCurve', curve_data)
        bpy.context.collection.objects.link(bpy_object)

        if not self.material1 is None:
            material_name = "NoiseGradient"
            mat = bpy.data.materials.new(name=material_name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links

            for node in nodes:
                nodes.remove(node)

            output_node = nodes.new(type='ShaderNodeOutputMaterial')
            output_node.location = (400, 0)

            bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
            bsdf_node.location = (0, -100)
            bsdf_node.inputs['Emission Strength'].default_value = self.emission_strength

            noise_texture_node = nodes.new(type='ShaderNodeTexNoise')
            noise_texture_node.location = (-400, 100)
            noise_texture_node.inputs["Scale"].default_value = 20.0
            noise_texture_node.inputs["Detail"].default_value = 2.0


            mapping_node = nodes.new(type='ShaderNodeMapping')
            mapping_node.location = (-600, 100)
            mapping_node.inputs["Scale"].default_value = (0.1, 1, 1)


            tex_coord_node = nodes.new(type='ShaderNodeTexCoord')
            tex_coord_node.location = (-800, 100)


            # transparent node
            transparent_node = nodes.new(type='ShaderNodeValToRGB')
            transparent_node.location = (-200, 100)
            transparent_node.color_ramp.interpolation = 'CONSTANT'

            transparent_node.color_ramp.elements[0].position = 0.2
            transparent_node.color_ramp.elements[0].color = (0, 0, 0, 1)
            transparent_node.color_ramp.elements[1].position = 0.6
            transparent_node.color_ramp.elements[1].color = (1, 1, 1, 1)

            # color node
            color_ramp_node = nodes.new(type='ShaderNodeValToRGB')
            color_ramp_node.location = (-200, 50)
            color_ramp_node.color_ramp.color_mode = 'HSL'
            color_ramp_node.color_ramp.hue_interpolation = 'CW'

            color_ramp_node.color_ramp.elements[0].position = 0.0
            color_ramp_node.color_ramp.elements[0].color = self.material1["Base Color"]
            color_ramp_node.color_ramp.elements[1].position = 1.0
            if not self.material2 is None:
                color_ramp_node.color_ramp.elements[1].color = self.material2["Base Color"]
            else:
                color_ramp_node.color_ramp.elements[1].color = self.material1["Base Color"]

            links.new(tex_coord_node.outputs['UV'], mapping_node.inputs['Vector'])
            links.new(mapping_node.outputs['Vector'], noise_texture_node.inputs['Vector'])
            links.new(noise_texture_node.outputs['Fac'], transparent_node.inputs['Fac'])

            links.new(noise_texture_node.outputs['Color'], color_ramp_node.inputs['Fac'])
            links.new(transparent_node.outputs['Color'], bsdf_node.inputs['Alpha'])
            links.new(color_ramp_node.outputs['Color'], bsdf_node.inputs['Base Color'])
            links.new(color_ramp_node.outputs['Color'], bsdf_node.inputs['Emission Color'])

            links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])

            bpy_object.data.materials.append(mat)

        if not self.rename is None:
            bpy_object.name = self.rename

        return bpy_object

if __name__ == "__main__":
    start_blender()

    ribbon = LinesFlow([(0, 0, 1), (2, 2, 1), (4, 3, 1), (6, 2, 1), (8, 0, 1)], width=0.2, material1=Si, material2=Si)
    ribbon_obj = ribbon.draw()

    cam = add_camera(ribbon_obj, angle=0, distance=8, light_distance=10, light_energy=10)

    cycles_render('D:/GithubProjects/blender-pyscripts-learning/test/linesflowtest/images/test.png', cam,
                  resolution_x=960, resolution_y=540)

    save_blender("./test.blend")


