import bpy
from bpycanvas import save_blender, start_blender

if __name__ == "__main__":
    start_blender()
    # 创建一个立方体
    bpy.ops.mesh.primitive_cube_add(size=2)

    save_blender("./test.blender")
