import bpy

def cut(obj_1, obj_2, solver="EXACT"):
    bool_modifier = obj_1.modifiers.new(name="Boolean_Cut", type='BOOLEAN')
    bool_modifier.object = obj_2
    bool_modifier.operation = 'DIFFERENCE'
    bool_modifier.solver = solver

    bpy.context.view_layer.objects.active = obj_1
    bpy.ops.object.modifier_apply(modifier=bool_modifier.name)

    bpy.data.objects.remove(obj_2)

    return obj_1

def add(obj_1, obj_2):
    bool_modifier = obj_1.modifiers.new(name="Boolean_Add", type='BOOLEAN')
    bool_modifier.object = obj_2
    bool_modifier.operation = 'UNION'

    bpy.context.view_layer.objects.active = obj_1
    bpy.ops.object.modifier_apply(modifier=bool_modifier.name)

    bpy.data.objects.remove(obj_2)

    return obj_1