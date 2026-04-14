import bpy
import bmesh
import numpy as np
import mapbox_earcut as earcut
from shapely.geometry import Polygon as SPolygon, MultiPolygon, GeometryCollection

import math

def remove_near_duplicate_points(coords, eps=1e-8):
    if not coords:
        return coords

    cleaned = [coords[0]]
    for p in coords[1:]:
        px, py = cleaned[-1]
        x, y = p
        if abs(x - px) > eps or abs(y - py) > eps:
            cleaned.append((x, y))

    # 如果最后一个和第一个太近，也去掉最后一个
    if len(cleaned) > 1:
        x0, y0 = cleaned[0]
        x1, y1 = cleaned[-1]
        if abs(x0 - x1) < eps and abs(y0 - y1) < eps:
            cleaned.pop()

    return cleaned


def remove_collinear_points(coords, eps=1e-12):
    """
    去掉严格或近似共线的中间点
    """
    if len(coords) < 3:
        return coords

    result = []
    n = len(coords)

    for i in range(n):
        p_prev = coords[i - 1]
        p = coords[i]
        p_next = coords[(i + 1) % n]

        x1, y1 = p_prev
        x2, y2 = p
        x3, y3 = p_next

        # 叉积接近 0 -> 共线
        cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

        if abs(cross) > eps:
            result.append(p)

    return result


def clean_ring(coords, eps_dup=1e-8, eps_collinear=1e-12):
    coords = list(coords)

    # shapely 的 ring 最后一个点通常和第一个点重复
    if len(coords) >= 2 and coords[0] == coords[-1]:
        coords = coords[:-1]

    coords = remove_near_duplicate_points(coords, eps=eps_dup)
    coords = remove_collinear_points(coords, eps=eps_collinear)

    return coords

def recalc_normals_outside(obj):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')


def add_solidify(obj, z_start, z_end):
    z_height = abs(z_end - z_start)

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    mod = obj.modifiers.new(name='Solidify', type='SOLIDIFY')
    mod.thickness = z_height
    mod.offset = 1.0 if z_end >= z_start else -1.0

    if hasattr(mod, "use_even_offset"):
        mod.use_even_offset = True
    if hasattr(mod, "use_quality_normals"):
        mod.use_quality_normals = True

    bpy.ops.object.modifier_apply(modifier=mod.name)
    obj.select_set(False)
    return obj


def polygon_to_mesh_object_earcut(poly, name="Polygon", z_start=0.0, z_end=1.0):
    """
    poly: shapely Polygon（支持 holes）
    """
    if poly.is_empty:
        return None

    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    rings = []

    ext = clean_ring(poly.exterior.coords, eps_dup=1e-7, eps_collinear=1e-10)
    if len(ext) >= 3:
        rings.append(ext)

    for interior in poly.interiors:
        hole = clean_ring(interior.coords, eps_dup=1e-7, eps_collinear=1e-10)
        if len(hole) >= 3:
            rings.append(hole)

    # earcut 输入
    vertices = []
    ring_end_indices = []
    total = 0

    for ring in rings:
        for x, y in ring:
            vertices.append([float(x), float(y)])
        total += len(ring)
        ring_end_indices.append(total)

    vertices = np.array(vertices, dtype=np.float64)
    ring_end_indices = np.array(ring_end_indices, dtype=np.uint32)

    # 三角化，返回扁平索引 [i0, i1, i2, i3, i4, i5, ...]
    tri_indices = earcut.triangulate_float64(vertices, ring_end_indices)

    bm = bmesh.new()
    bm_verts = [bm.verts.new((x, y, z_start)) for x, y in vertices]
    bm.verts.ensure_lookup_table()

    for i in range(0, len(tri_indices), 3):
        i0, i1, i2 = tri_indices[i:i+3]
        try:
            bm.faces.new((bm_verts[i0], bm_verts[i1], bm_verts[i2]))
        except ValueError:
            pass

    bm.faces.ensure_lookup_table()
    bm.to_mesh(mesh)
    bm.free()

    recalc_normals_outside(obj)
    obj = add_solidify(obj, z_start, z_end)
    recalc_normals_outside(obj)

    return obj


def shapely_to_mesh_object_fast(geom, name="PolygonResult", z_start=0.0, z_end=1.0):
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

    created = []
    for idx, poly in enumerate(polygons):
        if poly.is_empty:
            continue

        # 修一下脏几何
        if not poly.is_valid:
            poly = poly.buffer(0)

        poly = poly.simplify(1e-2, preserve_topology=True)

        if poly.is_empty:
            continue

        obj = polygon_to_mesh_object_earcut(
            poly,
            name=f"{name}_{idx}",
            z_start=z_start,
            z_end=z_end,
        )
        if obj is not None:
            created.append(obj)

    if not created:
        return None

    if len(created) == 1:
        return created[0]

    bpy.ops.object.select_all(action='DESELECT')
    for obj in created:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = created[0]
    bpy.ops.object.join()
    return created[0]

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