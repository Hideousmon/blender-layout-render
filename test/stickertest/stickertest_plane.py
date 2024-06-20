import bpy
import math
from bpycanvas import *

if __name__ == "__main__":
    start_blender()

    # Step 1: 创建一个平板对象
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
    plane = bpy.context.active_object

    # Step 2: 创建一个新的材质并启用节点
    material = bpy.data.materials.new(name="TransparentImageMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes

    # 移除默认的 Principled BSDF 节点
    nodes.remove(nodes.get('Principled BSDF'))

    # 创建所需的节点
    output_node = nodes.get('Material Output')
    transparent_bsdf_node = nodes.new(type='ShaderNodeBsdfTransparent')
    image_texture_node = nodes.new(type='ShaderNodeTexImage')
    diffuse_bsdf_node = nodes.new(type='ShaderNodeBsdfDiffuse')
    mix_shader_node = nodes.new(type='ShaderNodeMixShader')

    # 加载图片
    image = bpy.data.images.load('D:\\GithubProjects\\blender-pyscripts-learning\\test\\stickertest\\images\\Figure_2.png')
    image_texture_node.image = image

    # 配置节点
    node_tree = material.node_tree
    links = node_tree.links

    # 连接图片节点到混合节点
    links.new(image_texture_node.outputs['Color'], diffuse_bsdf_node.inputs['Color'])
    links.new(image_texture_node.outputs['Alpha'], mix_shader_node.inputs['Fac'])
    links.new(transparent_bsdf_node.outputs[0], mix_shader_node.inputs[1])
    links.new(diffuse_bsdf_node.outputs[0], mix_shader_node.inputs[2])
    links.new(mix_shader_node.outputs[0], output_node.inputs[0])

    # Step 3: 将材质应用到平板对象的顶部
    if plane.data.materials:
        plane.data.materials[0] = material
    else:
        plane.data.materials.append(material)

    # Step 4: 配置透明度
    material.blend_method = 'BLEND'
    material.shadow_method = 'CLIP'

    # Step 5: 调整平板的 UV 映射，使图片正确显示
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
    bpy.ops.object.mode_set(mode='OBJECT')

    save_blender("./test.blend")