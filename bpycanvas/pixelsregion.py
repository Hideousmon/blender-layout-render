from .utils import *
from .boolean import cut
from .filledpattern import Circle, Rectangle
import numpy as np
import os
import time

class CirclePixelsRegion:
    def __init__(self, bottom_left_corner_point, top_right_corner_point, pixel_radius, z_start, z_end, material=None,
                 group_name = "pixels", matrix_mask = None):
        self.left_down_point = tuple_to_point(bottom_left_corner_point)
        self.right_up_point = tuple_to_point(top_right_corner_point)
        self.pixel_radius = pixel_radius
        self.__last_array = None
        self.__lastest_array = None
        self.material = material
        self.z_start = z_start
        self.z_end = z_end
        self.group_name = group_name
        if (type(matrix_mask) != type(None)):
            self.matrix_mask = np.array(matrix_mask, dtype=np.int32)
        else:
            self.matrix_mask = matrix_mask

    def draw(self, matrix):
        if (type(self.matrix_mask) != type(None)):
            enable_positions = np.where(np.transpose(self.matrix_mask) == 1)
            if (len(np.transpose(enable_positions)) != len(matrix)):
                raise Exception("The input matrix can not match the matrix_mask!")
            masked_matrix = self.matrix_mask.copy().astype(np.double)
            for i,position in enumerate(np.transpose(enable_positions)):
                masked_matrix[position[1], position[0]] = matrix[i]
        elif (len(matrix.shape) != 2):
            raise Exception("The input matrix should be two-dimensional when matrix_mask not specified!")
        else:
            masked_matrix = matrix

        self.block_x_length = np.abs(self.left_down_point.x - self.right_up_point.x) / masked_matrix.shape[0]
        self.block_y_length = np.abs(self.left_down_point.y - self.right_up_point.y) / masked_matrix.shape[1]
        self.x_start_point = self.left_down_point.x + self.block_x_length / 2
        self.y_start_point = self.right_up_point.y - self.block_y_length / 2

        obj_list = []
        for row in range(0, masked_matrix.shape[1]):
            for col in range(0, masked_matrix.shape[0]):
                center_point = Point(self.x_start_point+col*self.block_x_length,self.y_start_point-row*self.block_y_length)
                radius = self.pixel_radius * masked_matrix[col,row]
                if (radius <= 0.001):
                    radius = 0
                if (np.isclose(radius, self.pixel_radius) or radius > self.pixel_radius):
                    radius = self.pixel_radius
                if (~np.isclose(radius, 0)):
                    circle = Circle(center_point=center_point, radius=radius, z_start=self.z_start, z_end=self.z_end,
                                    material=None, rename=self.group_name + str(col) + "_" + str(row))
                    circle_obj = circle.draw()
                    obj_list.append(circle_obj)


        bpy.ops.object.select_all(action='DESELECT')
        for obj in obj_list:
            obj.select_set(True)

        obj_for_return = obj_list[
            int(masked_matrix.shape[1] / 2) * masked_matrix.shape[0] + int(masked_matrix.shape[0] / 2)]
        bpy.context.view_layer.objects.active = obj_for_return
        bpy.ops.object.join()

        if not self.material is None:
            material = bpy.data.materials.new(name=self.material["Name"])
            material.use_nodes = True
            mat_nodes = material.node_tree.nodes
            mat_links = material.node_tree.links
            obj_for_return.data.materials.append(material)

            mat_nodes["Principled BSDF"].inputs["Metallic"].default_value = self.material["Metallic"]
            mat_nodes["Principled BSDF"].inputs["Base Color"].default_value = self.material["Base Color"]
            mat_nodes["Principled BSDF"].inputs["Roughness"].default_value = self.material["Roughness"]
            mat_nodes["Principled BSDF"].inputs["IOR"].default_value = self.material["IOR"]
            mat_nodes["Principled BSDF"].inputs["Alpha"].default_value = self.material["Alpha"]
            material.diffuse_color = self.material["Diffusion Color"]

        return obj_for_return

    def fast_draw_and_cut(self, obj_for_cut, matrix):
        if (type(self.matrix_mask) != type(None)):
            enable_positions = np.where(np.transpose(self.matrix_mask) == 1)
            if (len(np.transpose(enable_positions)) != len(matrix)):
                raise Exception("The input matrix can not match the matrix_mask!")
            masked_matrix = self.matrix_mask.copy().astype(np.double)
            for i,position in enumerate(np.transpose(enable_positions)):
                masked_matrix[position[1], position[0]] = matrix[i]
        elif (len(matrix.shape) != 2):
            raise Exception("The input matrix should be two-dimensional when matrix_mask not specified!")
        else:
            masked_matrix = matrix

        self.block_x_length = np.abs(self.left_down_point.x - self.right_up_point.x) / masked_matrix.shape[0]
        self.block_y_length = np.abs(self.left_down_point.y - self.right_up_point.y) / masked_matrix.shape[1]
        self.x_start_point = self.left_down_point.x + self.block_x_length / 2
        self.y_start_point = self.right_up_point.y - self.block_y_length / 2

        obj_list = []
        bpy.context.preferences.edit.use_global_undo = False
        view_layer = bpy.context.view_layer
        view_layer.update()

        for row in range(0, masked_matrix.shape[1]):
            for col in range(0, masked_matrix.shape[0]):
                center_point = Point(self.x_start_point+col*self.block_x_length,self.y_start_point-row*self.block_y_length)
                radius = self.pixel_radius * masked_matrix[col,row]
                if (radius <= 0.001):
                    radius = 0
                if (np.isclose(radius, self.pixel_radius) or radius > self.pixel_radius):
                    radius = self.pixel_radius
                if (~np.isclose(radius, 0)):

                    bpy.ops.mesh.primitive_cylinder_add(
                        radius=radius,
                        depth=abs(self.z_end - self.z_start),
                        location=(center_point.x, center_point.y, (self.z_start + self.z_end) / 2),
                        vertices=16
                    )

                    cyl = bpy.context.object

                    obj_list.append(cyl)

                if col == 0 and len(obj_list)!=0:
                    bpy.ops.object.select_all(action='DESELECT')
                    for obj in obj_list:
                        obj.select_set(True)
                    obj_for_return = obj_list[0]
                    bpy.context.view_layer.objects.active = obj_for_return
                    bpy.ops.object.join()
                    obj_for_cut = cut(obj_for_cut, obj_for_return)
                    print(f"finished row:", row)
                    obj_list =[]
            if row == masked_matrix.shape[1] - 1 and row != 0:
                bpy.ops.object.select_all(action='DESELECT')
                for obj in obj_list:
                    obj.select_set(True)
                obj_for_return = obj_list[0]
                bpy.context.view_layer.objects.active = obj_for_return
                bpy.ops.object.join()
                obj_for_cut = cut(obj_for_cut, obj_for_return)
                print(f"finished row:", row)
                obj_list = []

        return obj_for_cut

class RectanglePixelsRegion:
    def __init__(self, bottom_left_corner_point, top_right_corner_point, pixel_x_length, pixel_y_length, z_start, z_end,
                 material=None, group_name = "p", matrix_mask = None):
        self.left_down_point = tuple_to_point(bottom_left_corner_point)
        self.right_up_point = tuple_to_point(top_right_corner_point)
        self.pixel_x_length = pixel_x_length
        self.pixel_y_length = pixel_y_length
        self.__last_array = None
        self.__lastest_array = None
        self.material = material
        self.z_start = z_start
        self.z_end = z_end
        self.group_name = group_name
        if (type(matrix_mask) != type(None)):
            self.matrix_mask = np.array(matrix_mask, dtype=np.int32)
        else:
            self.matrix_mask = matrix_mask

    def draw(self, matrix):
        if (type(self.matrix_mask) != type(None)):
            enable_positions = np.where(np.transpose(self.matrix_mask) == 1)
            if (len(np.transpose(enable_positions)) != len(matrix)):
                raise Exception("The input matrix can not match the matrix_mask!")
            masked_matrix = self.matrix_mask.copy().astype(np.double)
            for i,position in enumerate(np.transpose(enable_positions)):
                masked_matrix[position[1], position[0]] = matrix[i]
        elif (len(matrix.shape) != 2):
            raise Exception("The input matrix should be two-dimensional when matrix_mask not specified!")
        else:
            masked_matrix = matrix

        self.block_x_length = np.abs(self.left_down_point.x - self.right_up_point.x) / masked_matrix.shape[0]
        self.block_y_length = np.abs(self.left_down_point.y - self.right_up_point.y) / masked_matrix.shape[1]
        self.x_start_point = self.left_down_point.x + self.block_x_length / 2
        self.y_start_point = self.right_up_point.y - self.block_y_length / 2

        obj_list = []
        for row in range(0, masked_matrix.shape[1]):
            for col in range(0, masked_matrix.shape[0]):
                center_point = Point(self.x_start_point + col * self.block_x_length,
                                     self.y_start_point - row * self.block_y_length)
                x_length = self.pixel_x_length * masked_matrix[col, row]
                y_length = self.pixel_y_length * masked_matrix[col, row]
                if (x_length < 0.001):
                    x_length = 0
                if (y_length < 0.001):
                    y_length = 0
                if (np.isclose(x_length, self.pixel_x_length) or x_length > self.pixel_x_length):
                    x_length = self.pixel_x_length
                if (np.isclose(y_length, self.pixel_y_length) or y_length > self.pixel_y_length):
                    y_length = self.pixel_y_length
                if (~np.isclose(x_length, 0) and ~np.isclose(y_length, 0)):
                    rect = Rectangle(center_point=center_point, width=x_length, height=y_length,
                                     z_start=self.z_start, z_end=self.z_end,
                                    material=None, rename=self.group_name + str(col) + "_" + str(row))
                    rect_obj = rect.draw()
                    obj_list.append(rect_obj)


        bpy.ops.object.select_all(action='DESELECT')
        for obj in obj_list:
            obj.select_set(True)

        obj_for_return = obj_list[int(masked_matrix.shape[1]/2)*masked_matrix.shape[0] + int(masked_matrix.shape[0]/2)]
        bpy.context.view_layer.objects.active = obj_for_return
        bpy.ops.object.join()

        if not self.material is None:
            material = bpy.data.materials.new(name=self.material["Name"])
            material.use_nodes = True
            mat_nodes = material.node_tree.nodes
            mat_links = material.node_tree.links
            obj_for_return.data.materials.append(material)

            mat_nodes["Principled BSDF"].inputs["Metallic"].default_value = self.material["Metallic"]
            mat_nodes["Principled BSDF"].inputs["Base Color"].default_value = self.material["Base Color"]
            mat_nodes["Principled BSDF"].inputs["Roughness"].default_value = self.material["Roughness"]
            mat_nodes["Principled BSDF"].inputs["IOR"].default_value = self.material["IOR"]
            mat_nodes["Principled BSDF"].inputs["Alpha"].default_value = self.material["Alpha"]
            material.diffuse_color = self.material["Diffusion Color"]

        return obj_for_return


