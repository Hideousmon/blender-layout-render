from .utils import *
from .material import *
import bpy

class HoldesLikeSurface:
    def __init__(self, x_start, x_end, r_of_x, nu=80, nv=40,
                 material=None, rename=None):
        self.x_start = x_start
        self.x_end = x_end
        self.r_of_x = r_of_x
        self.nu = nu
        self.nv = nv
        self.material = material
        self.rename = rename
        if x_start == x_end:
            self.ifexist = 0
        else:
            self.ifexist = 1

        self.verts = []
        self.faces = []

        def vid(i, j):
            return j * self.nu + (i % self.nu)

        for j in range(self.nv):
            t = j / (self.nv - 1)
            v = self.x_start + (self.x_end - self.x_start) * t
            r = self.r_of_x(v)
            x = v

            for i in range(self.nu):
                u = 2.0 * math.pi * i / self.nu
                y = r * math.cos(u)
                z = r * math.sin(u)
                self.verts.append((x, y, z))

        for j in range(self.nv - 1):
            for i in range(self.nu):
                self.faces.append((
                    vid(i, j),
                    vid(i + 1, j),
                    vid(i + 1, j + 1),
                    vid(i, j + 1),
                ))

    def draw(self):

        mesh = bpy.data.meshes.new("HLSMesh")
        mesh.from_pydata(self.verts, [], self.faces)
        mesh.update()

        bpy_object = bpy.data.objects.new("HLS", mesh)
        bpy.context.collection.objects.link(bpy_object)
        for p in mesh.polygons:
            p.use_smooth = True

        wire = bpy_object.copy()
        wire.data = bpy_object.data.copy()
        bpy.context.collection.objects.link(wire)
        mod = wire.modifiers.new(name="Wireframe", type='WIREFRAME')
        mod.thickness = 0.01
        mod.use_replace = True
        mod.use_even_offset = True
        wire_mat = bpy.data.materials.get("WormholeWireMat")
        if wire_mat is None:
            wire_mat = bpy.data.materials.new("WormholeWireMat")

        wire_mat.use_nodes = True
        nodes = wire_mat.node_tree.nodes
        links = wire_mat.node_tree.links
        nodes.clear()

        out = nodes.new("ShaderNodeOutputMaterial")
        out.location = (350, 0)

        emission = nodes.new("ShaderNodeEmission")
        emission.location = (100, 0)
        emission.inputs["Color"].default_value = (0.75, 0.82, 1.0, 1.0)
        emission.inputs["Strength"].default_value = 0.9

        links.new(emission.outputs["Emission"], out.inputs["Surface"])

        wire.data.materials.clear()
        wire.data.materials.append(wire_mat)

        wire.scale = (1.001, 1.001, 1.001)



        solid = bpy_object.modifiers.new(name="Solidify", type='SOLIDIFY')
        solid.thickness = 0.08  # 厚度
        solid.offset = 0.0  # 0 表示向两侧平均加厚；1 / -1 表示偏向一侧
        solid.use_even_offset = True
        solid.use_quality_normals = True
        bpy.context.view_layer.objects.active = bpy_object
        bpy_object.select_set(True)
        bpy.ops.object.modifier_apply(modifier=solid.name)

        if not self.material is None:
            material = bpy.data.materials.new(name=self.material["Name"])
            material.use_nodes = True
            mat_nodes = material.node_tree.nodes
            mat_links = material.node_tree.links
            bpy_object.data.materials.append(material)

            mat_nodes["Principled BSDF"].inputs["Metallic"].default_value = self.material["Metallic"]
            mat_nodes["Principled BSDF"].inputs["Base Color"].default_value = self.material["Base Color"]
            mat_nodes["Principled BSDF"].inputs["Roughness"].default_value = self.material["Roughness"]
            mat_nodes["Principled BSDF"].inputs["IOR"].default_value = self.material["IOR"]
            mat_nodes["Principled BSDF"].inputs["Alpha"].default_value = self.material["Alpha"]
            material.diffuse_color = self.material["Diffusion Color"]
        if not self.rename is None:
            bpy_object.name = self.rename

        return bpy_object
