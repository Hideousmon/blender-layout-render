from .utils import *
from .material import *
import bpy

class StickerPlane:
    def __init__(self, center_point, image_path, width = 1.0, height = 0.8, z_center = 0.111, rename=None):
        self.start_point = tuple_to_point(center_point)
        self.image_path = image_path
        self.width = width
        self.height = height
        self.z_center = z_center
        self.rename = rename

        self.location = (center_point.x, center_point.y, z_center)
        self.scale = (width, height, 1)


    def draw(self):
        bpy.ops.mesh.primitive_plane_add(size=1, location=self.location)
        bpy_object = bpy.context.active_object
        bpy_object.scale = self.scale

        material = bpy.data.materials.new(name="TransparentImageMaterial")
        material.use_nodes = True
        nodes = material.node_tree.nodes

        nodes.remove(nodes.get('Principled BSDF'))

        output_node = nodes.get('Material Output')
        transparent_bsdf_node = nodes.new(type='ShaderNodeBsdfTransparent')
        image_texture_node = nodes.new(type='ShaderNodeTexImage')
        diffuse_bsdf_node = nodes.new(type='ShaderNodeBsdfDiffuse')
        mix_shader_node = nodes.new(type='ShaderNodeMixShader')

        image = bpy.data.images.load(self.image_path)
        image_texture_node.image = image

        node_tree = material.node_tree
        links = node_tree.links

        links.new(image_texture_node.outputs['Color'], diffuse_bsdf_node.inputs['Color'])
        links.new(image_texture_node.outputs['Alpha'], mix_shader_node.inputs['Fac'])
        links.new(transparent_bsdf_node.outputs[0], mix_shader_node.inputs[1])
        links.new(diffuse_bsdf_node.outputs[0], mix_shader_node.inputs[2])
        links.new(mix_shader_node.outputs[0], output_node.inputs[0])

        if bpy_object.data.materials:
            bpy_object.data.materials[0] = material
        else:
            bpy_object.data.materials.append(material)

        material.blend_method = 'BLEND'
        material.shadow_method = 'CLIP'

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.object.mode_set(mode='OBJECT')

        if not self.rename is None:
            bpy_object.name = self.rename

        return bpy_object
