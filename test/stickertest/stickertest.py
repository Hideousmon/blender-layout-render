import bpy
import math
from bpycanvas import *

if __name__ == "__main__":
    start_blender()

    # Step 1: 创建一个简单的立方体对象
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    cube = bpy.context.active_object

    # Step 2: 创建一个新的材质
    material = bpy.data.materials.new(name="TransparentImageMaterial")
    material.use_nodes = True
    nodes = material.node_tree.nodes

    # 移除默认的 diffuse BSDF 节点
    nodes.remove(nodes.get('Principled BSDF'))

    # 创建所需的节点
    output_node = nodes.get('Material Output')
    bsdf_node = nodes.new(type='ShaderNodeBsdfTransparent')
    image_node = nodes.new(type='ShaderNodeTexImage')
    mix_shader = nodes.new(type='ShaderNodeMixShader')

    # 加载图片
    image = bpy.data.images.load('D:\\GithubProjects\\blender-pyscripts-learning\\test\\stickertest\\images\\Figure_2.png')
    image_node.image = image

    # 配置节点
    node_tree = material.node_tree
    links = node_tree.links

    links.new(image_node.outputs['Color'], mix_shader.inputs[2])
    links.new(bsdf_node.outputs[0], mix_shader.inputs[1])
    links.new(mix_shader.outputs[0], output_node.inputs[0])
    links.new(image_node.outputs['Alpha'], mix_shader.inputs['Fac'])

    # Step 3: 将材质应用到对象的表面
    if cube.data.materials:
        cube.data.materials[0] = material
    else:
        cube.data.materials.append(material)

    # Step 4: 配置透明度
    bpy.context.object.active_material.blend_method = 'BLEND'
    bpy.context.object.active_material.shadow_method = 'CLIP'

    # Step 5: 调整对象的 UV 映射，使图片正确显示
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
    bpy.ops.object.mode_set(mode='OBJECT')

    save_blender("./test.blend")