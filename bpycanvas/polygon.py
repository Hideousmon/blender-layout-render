from .utils import *
import numpy as np
import bpy
import bmesh

class Polygon:
    def __init__(self, point_list, z_start, z_end, material = None, rename = None,
                 start_point = None, end_point = None, input_point = None, through_point = None,
                 drop_point = None, add_point = None):
        self.point_list = []
        self.tuple_list = []
        if (type(point_list) == np.ndarray):
            point_list = point_list.tolist()
        for item in point_list:
            if type(item) == Point:
                self.tuple_list.append(item.to_tuple())
                self.point_list.append(item)
            elif type(item) == tuple:
                self.tuple_list.append(item)
                self.point_list.append(Point(item[0],item[1]))
            elif type(item) == list:
                self.tuple_list.append(tuple(item))
                self.point_list.append(Point(item[0], item[1]))
            elif type(item) == np.ndarray:
                self.tuple_list.append(tuple(item))
                self.point_list.append(Point(item[0], item[1]))
            else:
                raise Exception("Polygon Wrong Type Input!")
        self.z_start = z_start
        self.z_end = z_end
        self.material = material
        self.rename = rename
        self.start_point = tuple_to_point(start_point)
        self.end_point = tuple_to_point(end_point)
        self.input_point = tuple_to_point(input_point)
        self.through_point = tuple_to_point(through_point)
        self.drop_point = tuple_to_point(drop_point)
        self.add_point = tuple_to_point(add_point)

    def draw(self):
        mesh = bpy.data.meshes.new("Polygon")
        polygon_obj = bpy.data.objects.new("Polygon", mesh)
        bpy.context.collection.objects.link(polygon_obj)

        bm = bmesh.new()

        segments = len(self.point_list)
        z_center = (self.z_start + self.z_end)/2
        z_height = abs(self.z_end - self.z_start)

        bm_verts = []
        for i in range(segments):
            bm_verts.append(bm.verts.new((self.point_list[i].x, self.point_list[i].y, z_center)))

        bm.verts.ensure_lookup_table()
        bm.faces.new(bm_verts)
        bm.faces.ensure_lookup_table()

        # for i in range(segments):
        #     bm.edges.new((bm.verts[i], bm.verts[(i + 1)%segments]))
        bm.to_mesh(mesh)
        bm.free()
        # bpy.ops.object.select_all(action='DESELECT')
        # obj.select_set(True)
        bpy.context.view_layer.objects.active = polygon_obj
        # bpy.ops.object.convert(target='MESH')
        # bpy.ops.object.mode_set(mode='EDIT')
        # bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, z_height)})
        # bpy.ops.object.mode_set(mode='OBJECT')
        # bpy.ops.object.modifier_add(type='SOLIDIFY')
        # bpy.context.object.modifiers["Solidify"].thickness = z_height
        # bpy.ops.object.modifier_apply(modifier="Solidify")

        bpy.ops.object.mode_set(mode='OBJECT')

        # 添加 SOLIDIFY 修改器以增加厚度
        solidify_modifier = polygon_obj.modifiers.new(name='Solidify', type='SOLIDIFY')
        solidify_modifier.thickness = z_height  # 设置厚度

        # 应用 SOLIDIFY 修改器
        bpy.ops.object.modifier_apply(modifier=solidify_modifier.name)

        if not (self.material == None):
            material = bpy.data.materials.new(name=self.material["Name"])
            material.use_nodes = True
            mat_nodes = material.node_tree.nodes
            mat_links = material.node_tree.links
            polygon_obj.data.materials.append(material)

            mat_nodes["Principled BSDF"].inputs["Metallic"].default_value = self.material["Metallic"]
            mat_nodes["Principled BSDF"].inputs["Base Color"].default_value = self.material["Base Color"]
            mat_nodes["Principled BSDF"].inputs["Roughness"].default_value = self.material["Roughness"]
            mat_nodes["Principled BSDF"].inputs["IOR"].default_value = self.material["IOR"]
            mat_nodes["Principled BSDF"].inputs["Alpha"].default_value = self.material["Alpha"]
            material.diffuse_color = self.material["Diffusion Color"]
        if not (self.rename == None):
            polygon_obj.name = self.rename

        return polygon_obj

    def get_the_point_at_number(self,i):
        if (i >= len(self.point_list)):
            raise Exception("The Request Polygon Point not Exist!")
        return self.point_list[i]

    def get_start_point(self):
        if (type(self.start_point) == type(None)):
            raise Exception("\"start_point\" is not specified in this Polygon!")
        else:
            return self.start_point

    def get_end_point(self):
        if (type(self.end_point) == type(None)):
            raise Exception("\"end_point\" is not specified in this Polygon!")
        else:
            return self.end_point

    def get_input_point(self):
        if (type(self.input_point) == type(None)):
            raise Exception("\"input_point\" is not specified in this Polygon!")
        else:
            return self.input_point

    def get_through_point(self):
        if (type(self.through_point) == type(None)):
            raise Exception("\"through_point\" is not specified in this Polygon!")
        else:
            return self.through_point

    def get_drop_point(self):
        if (type(self.drop_point) == type(None)):
            raise Exception("\"drop_point\" is not specified in this Polygon!")
        else:
            return self.drop_point

    def get_add_point(self):
        if (type(self.add_point) == type(None)):
            raise Exception("\"add_point\" is not specified in this Polygon!")
        else:
            return self.add_point