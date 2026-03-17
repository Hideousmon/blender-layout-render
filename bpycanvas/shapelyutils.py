import bpy
import bmesh
from shapely.geometry import Polygon as SPolygon, MultiPolygon, GeometryCollection
from shapely.ops import triangulate

def _signed_area_2d(coords):
    area = 0.0
    n = len(coords)
    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return area * 0.5

def _ensure_ccw(coords):
    return coords if _signed_area_2d(coords) > 0 else coords[::-1]

def _ensure_cw(coords):
    return coords if _signed_area_2d(coords) < 0 else coords[::-1]



def _add_solidify(obj, z_start, z_end):
    z_height = abs(z_end - z_start)

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    solidify_modifier = obj.modifiers.new(name='Solidify', type='SOLIDIFY')
    solidify_modifier.thickness = z_height
    solidify_modifier.offset = 1.0 if z_end >= z_start else -1.0

    # 尽量贴近你原来的 mesh 厚化风格
    if hasattr(solidify_modifier, "use_even_offset"):
        solidify_modifier.use_even_offset = True
    if hasattr(solidify_modifier, "use_quality_normals"):
        solidify_modifier.use_quality_normals = True

    bpy.ops.object.modifier_apply(modifier=solidify_modifier.name)
    obj.select_set(False)
    return obj


def _polygon_to_mesh_object_no_hole(poly, name="Polygon", z_start=0.0, z_end=1.0):
    """
    仅适用于没有孔的 shapely Polygon
    """
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    coords = list(poly.exterior.coords)[:-1][::-1]
    bm_verts = [bm.verts.new((x, y, z_start)) for x, y in coords]

    bm.verts.ensure_lookup_table()
    bm.faces.new(bm_verts)

    bm.to_mesh(mesh)
    bm.free()

    return _add_solidify(obj, z_start, z_end)


def _polygon_to_mesh_object_triangulated(poly, name="Polygon", z_start=0.0, z_end=1.0):
    """
    适用于有孔 polygon：先三角化，再建 mesh
    """
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    vert_cache = {}

    def get_vert(x, y):
        key = (round(float(x), 10), round(float(y), 10))
        if key not in vert_cache:
            vert_cache[key] = bm.verts.new((x, y, z_start))
        return vert_cache[key]

    # shapely triangulate 会生成覆盖凸包的三角形，所以要过滤：
    # 仅保留 “完全落在原 polygon 内部”的三角形
    tris = triangulate(poly)

    for tri in tris:
        # 用 representative_point / centroid 过滤都行
        if not tri.representative_point().within(poly):
            continue

        coords = list(tri.exterior.coords)[:-1]
        if len(coords) != 3:
            continue

        try:
            face_verts = [get_vert(x, y) for x, y in coords]
            bm.faces.new(face_verts)
        except ValueError:
            # face 已存在时跳过
            pass

    bm.verts.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    bm.to_mesh(mesh)
    bm.free()

    return _add_solidify(obj, z_start, z_end)


def shapely_to_mesh_object(geom, name="PolygonResult", z_start=0.0, z_end=1.0):
    """
    Polygon / MultiPolygon / GeometryCollection -> Blender Mesh
    """
    if geom.is_empty:
        return None

    polygons = []

    if geom.geom_type == 'Polygon':
        polygons = [geom]
    elif geom.geom_type == 'MultiPolygon':
        polygons = list(geom.geoms)
    elif geom.geom_type == 'GeometryCollection':
        polygons = [g for g in geom.geoms if g.geom_type == 'Polygon']
    else:
        return None

    created_objs = []

    for idx, poly in enumerate(polygons):
        if poly.is_empty:
            continue

        has_holes = len(poly.interiors) > 0

        if has_holes:
            obj = _polygon_to_mesh_object_triangulated(
                poly, name=f"{name}_{idx}", z_start=z_start, z_end=z_end
            )
        else:
            obj = _polygon_to_mesh_object_no_hole(
                poly, name=f"{name}_{idx}", z_start=z_start, z_end=z_end
            )

        created_objs.append(obj)

    if not created_objs:
        return None

    if len(created_objs) == 1:
        return created_objs[0]

    bpy.ops.object.select_all(action='DESELECT')
    for obj in created_objs:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = created_objs[0]
    bpy.ops.object.join()

    return created_objs[0]

def np_polygon_to_shapely(poly_xy):
    pts = [(float(x), float(y)) for x, y in poly_xy]
    if len(pts) < 3:
        return None

    geom = SPolygon(pts)

    if not geom.is_valid:
        geom = geom.buffer(0)

    if geom.is_empty:
        return None

    return geom