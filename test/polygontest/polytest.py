import bpy
from bpycanvas import save_blender, start_blender

if __name__ == "__main__":
    start_blender()
    # objectives
    bpy.ops.mesh.primitive_cube_add(size=3, location=(0, 0, 1.5))
    cube = bpy.context.active_object
    bpy.ops.mesh.primitive_plane_add(size=50)
    plane = bpy.context.active_object

    # add poly
    vertices = [(1.0, 1.0, 4.0), (1.0, -1.0, 4.0), (-1.0, -1.0, 4.0), (-1.0, 1.0, 4.0)]
    edges = []
    faces = [(0, 1, 2, 3)]

    mesh = bpy.data.meshes.new(name="Polygon")
    mesh.from_pydata(vertices, edges, faces)
    mesh.update()

    poly = bpy.data.objects.new(name="PolygonObject", object_data=mesh)

    # bpy.context.scene.collection.objects.link(obj)
    bpy.context.collection.objects.link(poly)

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

    # 设置渲染引擎为 Cycles
    bpy.context.scene.render.engine = 'CYCLES'

    # 设置渲染分辨率
    scene = bpy.context.scene
    scene.camera = cam
    scene.render.image_settings.file_format="PNG"
    scene.render.filepath = 'D:/GithubProjects/blender-pyscripts-learning/test/polygontest/images/test.png'
    scene.render.resolution_x = 480
    scene.render.resolution_y = 320

    # bpy.ops.render.render('INVOKE_DEFAULT',write_still=True)
    bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)

    save_blender("./test.blend")
