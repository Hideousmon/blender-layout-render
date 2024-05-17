import bpy
from bpycanvas import save_blender, start_blender

if __name__ == "__main__":
    start_blender()
    # 创建一个立方体
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))

    bpy.ops.mesh.primitive_cube_add(location=(0, 0, -0.05))

    bpy.context.object.scale[0] = 10
    bpy.context.object.scale[1] = 10
    bpy.context.object.scale[2] = 0.1
    material = bpy.data.materials.new(name="Material")
    material.diffuse_color = (1, 0, 0, 1)
    bpy.context.object.data.materials.append(material)

    # 添加相机
    cam_dat = bpy.data.cameras.new('camera')
    cam = bpy.data.objects.new('camera', cam_dat)
    cam.location = (0, 8, 8)
    cam.rotation_euler = (-0.8853, 0, 0)
    # bpy.ops.object.camera_add(location=(0, 8, 8),rotation=(-0.7853, 0, 0))
    bpy.ops.object.light_add(type='SUN', location=(0, 10, 10))
    bpy.context.scene.camera = cam

    bpy.context.window_manager.windows.update()

    # 设置渲染引擎为 Cycles
    bpy.context.scene.render.engine = 'CYCLES'

    # 设置渲染分辨率
    bpy.data.scenes["Scene"].render.filepath = 'D:/GithubProjects/blender-pyscripts-learning/test/rendertest/images/test.png'
    bpy.context.scene.render.resolution_x = 1280
    bpy.context.scene.render.resolution_y = 720

    bpy.ops.render.render('INVOKE_DEFAULT',write_still=True)

    save_blender("./test.blend")
