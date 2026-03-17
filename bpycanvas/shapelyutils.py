import bpy
from shapely.geometry import Polygon as SPolygon, MultiPolygon, GeometryCollection
from shapely.ops import unary_union


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

def shapely_to_curve_object(geom, name="PolygonResult", z_start=0.0, z_end=1.0):
    if geom.is_empty:
        return None

    curve_data = bpy.data.curves.new(name=name, type='CURVE')
    curve_data.dimensions = '2D'
    curve_data.fill_mode = 'BOTH'
    curve_data.extrude = max(0.0, z_end - z_start)

    def add_ring(coords, is_hole=False):
        coords = list(coords)
        if len(coords) < 4:
            return

        coords = coords[:-1]

        coords = _ensure_cw(coords) if is_hole else _ensure_ccw(coords)

        spline = curve_data.splines.new('POLY')
        spline.points.add(len(coords) - 1)
        for i, (x, y) in enumerate(coords):
            spline.points[i].co = (x, y, 0.0, 1.0)
        spline.use_cyclic_u = True

    polygons = []
    if geom.geom_type == 'Polygon':
        polygons = [geom]
    elif geom.geom_type == 'MultiPolygon':
        polygons = list(geom.geoms)
    elif geom.geom_type == 'GeometryCollection':
        polygons = [g for g in geom.geoms if g.geom_type in ('Polygon', 'MultiPolygon')]
    else:
        return None

    for poly in polygons:
        if poly.geom_type == 'MultiPolygon':
            for sub_poly in poly.geoms:
                add_ring(sub_poly.exterior.coords, is_hole=False)
                for interior in sub_poly.interiors:
                    add_ring(interior.coords, is_hole=True)
        else:
            add_ring(poly.exterior.coords, is_hole=False)
            for interior in poly.interiors:
                add_ring(interior.coords, is_hole=True)

    obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(obj)
    obj.location.z = z_start

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    obj.select_set(False)

    return obj

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