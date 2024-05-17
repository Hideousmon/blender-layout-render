import bpy
from bpycanvas import save_blender, start_blender, render

if __name__ == "__main__":
    start_blender()
    # objectives
    bpy.ops.mesh.primitive_cube_add(size=3, location=(0, 0, 1.5))
    cube = bpy.context.active_object
    bpy.ops.mesh.primitive_plane_add(size=50)
    plane = bpy.context.active_object

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
    constraint.target = cube

    bpy.context.collection.objects.link(cam)

    # add material cube
    material = bpy.data.materials.new(name="Material")
    material.use_nodes = True
    mat_nodes = material.node_tree.nodes
    mat_links = material.node_tree.links
    cube.data.materials.append(material)

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

    render('D:/GithubProjects/blender-pyscripts-learning/test/rendertest/images/test.png',
           scene_cam=cam, resolution_x=1920, resolution_y=1080)
    # # 设置渲染引擎为 Cycles
    # bpy.context.scene.render.engine = 'CYCLES'
    # bpy.context.scene.cycles.device = 'GPU'
    # cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
    # if hasattr(cycles_prefs, 'get_devices'):
    #     cycles_prefs.get_devices()
    # bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    # for device in cycles_prefs.devices:
    #     if device.type == 'CUDA':
    #         device.use = True
    #     else:
    #         device.use = False
    #     print(f"Device: {device.name}, Type: {device.type}, Use: {device.use}")
    #
    #
    # # # 配置 OPTIX 设备（如果适用）
    # # if cycles_prefs.compute_device_type == 'OPTIX':
    # #     bpy.context.scene.cycles.device = 'GPU'
    # #     cycles_prefs.get_devices()
    # #     for device in cycles_prefs.devices:
    # #         if device.type == 'OPTIX':
    # #             device.use = True
    # #
    # # # 配置 OpenCL 设备（如果适用）
    # # if cycles_prefs.compute_device_type == 'OPENCL':
    # #     bpy.context.scene.cycles.device = 'GPU'
    # #     cycles_prefs.get_devices()
    # #     for device in cycles_prefs.devices:
    # #         if device.type == 'OPENCL':
    # #             device.use = True
    #
    # # 设置渲染分辨率
    # scene = bpy.context.scene
    # scene.camera = cam
    # scene.render.image_settings.file_format="PNG"
    # scene.render.filepath = 'D:/GithubProjects/blender-pyscripts-learning/test/rendertest/images/test.png'
    # # scene.render.resolution_x = 480
    # # scene.render.resolution_y = 320
    # scene.render.resolution_x = 1920
    # scene.render.resolution_y = 1080
    #
    #
    # # bpy.ops.render.render('INVOKE_DEFAULT',write_still=True)
    # bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)

    save_blender("./test.blend")
