import bpy
import math
from bpycanvas import save_blender, start_blender, render

if __name__ == "__main__":
    start_blender()
    # objectives
    # bpy.ops.mesh.primitive_cube_add(size=3, location=(0, 0, 1.5))
    # cube = bpy.context.active_object
    bpy.ops.mesh.primitive_plane_add(size=50)
    plane = bpy.context.active_object

    # add arrow
    # 创建箭杆（圆柱体）
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.05,  # 箭杆半径
        depth=2,  # 箭杆长度
        location=(0, 0, 1)  # 将箭杆位置设置在世界中心（稍微向上移动）
    )
    arrow_shaft = bpy.context.object

    # 创建箭头（圆锥）
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.15,  # 底部半径
        depth=0.5,  # 高度
        location=(0, 0, 2.25)  # 将圆锥位置设置在箭杆顶部
    )
    arrow_head = bpy.context.object

    # 组合箭杆和箭头
    bpy.ops.object.select_all(action='DESELECT')
    arrow_shaft.select_set(True)
    arrow_head.select_set(True)
    bpy.context.view_layer.objects.active = arrow_shaft
    bpy.ops.object.join()  # 将箭杆和箭头组合成一个对象

    # 重命名组合后的箭头对象
    arrow = bpy.context.object
    arrow.name = "Arrow"
    arrow.rotation_euler = (math.radians(-90), 0, 0)


    # add light
    light_data = bpy.data.lights.new("light", type = "SUN")
    light = bpy.data.objects.new("light", light_data)
    bpy.context.collection.objects.link(light)
    light.location = (3, -4, 5)
    light.data.energy = 200.0

    # add camera
    cam_dat = bpy.data.cameras.new('camera')
    cam = bpy.data.objects.new('camera', cam_dat)
    cam.location = (25, -3, 20)
    constraint = cam.constraints.new(type='TRACK_TO')
    constraint.target = arrow

    bpy.context.collection.objects.link(cam)

    # add material cube
    material = bpy.data.materials.new(name="Material")
    material.use_nodes = True
    mat_nodes = material.node_tree.nodes
    mat_links = material.node_tree.links
    arrow.data.materials.append(material)

    mat_nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
    mat_nodes["Principled BSDF"].inputs["Base Color"].default_value = [255 / 255.0,
                                                                       97 / 255.0,
                                                                       3 / 255.0,
                                                                       1.0]
    mat_nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.167

    # add material plane
    material = bpy.data.materials.new(name="Material")
    material.use_nodes = True
    mat_nodes = material.node_tree.nodes
    mat_links = material.node_tree.links
    plane.data.materials.append(material)

    mat_nodes["Principled BSDF"].inputs["Base Color"].default_value = [0.01,
                                                                       0.065,
                                                                       0.800,
                                                                       1.0]
    mat_nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.5

    bpy.context.window_manager.windows.update()

    render('D:/GithubProjects/blender-pyscripts-learning/test/wgrendertest/images/test.png', cam)

    save_blender("./test.blend")
