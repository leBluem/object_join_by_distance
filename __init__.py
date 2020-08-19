bl_info = {
    "name": "Join Objects by distance",
    "author": "leBluem",
    "version": (0, 2),
    "blender": (2, 80, 0),
    "description": "Join selected objects by variable distance, optional: set origin to object, def. shortcut: J",
    "category": "Object",
    "url": "https://github.com/leBluem/object_join_by_distance"
}

import bpy, sys, math
from bpy.props import BoolProperty, EnumProperty, StringProperty, FloatProperty

def getDistance(p1, p2):
    return math.sqrt( (p2.x-p1.x) ** 2 + (p2.y-p1.y) ** 2 + (p2.z-p1.z) ** 2 )

def join_objects(self, context):
    selected_obj = bpy.context.selected_objects.copy()
    if len(selected_obj)>0:
        i1 = 0
        i2 = 0
        done = []
        joined = []
        if self.setOriginToObject:
            # bpy.data.objects[obj.name].origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        for obj in bpy.context.selected_objects:
            obj.select_set(False)

        for obj in selected_obj:
            if i1>0 and (not obj in done):
                i2 = i1 + 1
                for objINNER in selected_obj:
                    if i2>0 and (not objINNER in done) and objINNER!=obj:
                        distance = getDistance( obj.location, objINNER.location )
                        # print(str(round(distance,3)))
                        if distance < self.scaling:
                            # bpy.context.view_layer.objects.active = bpy.data.objects[obj.name]
                            bpy.context.view_layer.objects.active = obj
                            obj.select_set(True)
                            bpy.data.objects[objINNER.name].select_set(True) # 2.8+
                            done.append(objINNER)
                            bpy.ops.object.join()
                            joined.append(obj)
                            obj.select_set(False)
                            # bpy.ops.object.join(bpy.data.objects[objINNER.name])
                            # selected_obj[0].name
                    i2 += 1
            i1 += 1

        # select something so you see changes
        i = 0
        for obj in selected_obj:
            if not obj in done:
                if i==0:
                    bpy.context.view_layer.objects.active = obj
                    i += 1
                obj.select_set(True)

        # select more? nah!
        # for obj in joined:
        #     if not obj in done:
        #         if i==0:
        #             bpy.context.view_layer.objects.active = obj
        #             i += 1
        #         obj.select_set(True)
    else:
        print('Nothing selected!')

class JoinByDistance(bpy.types.Operator):
    """Join by distance"""
    bl_idname = "object.join_by_distance"
    bl_label = "Join objects by distance"
    bl_options = {'REGISTER', 'UNDO'}

    scaling     : FloatProperty(
        name="Distance",
        description="minimal distance between objects",
        min=0.0,
        max=10000000.0,
        default=0.01
        )
    setOriginToObject : BoolProperty(
        name="Set Origin to Object center first",
        description="if object origin is somewhere else",
        default=1
        )

    def execute(self, context):
        join_objects(self, context)
        return {'FINISHED'}

addon_keymaps = []

# Register
classes = [
    JoinByDistance
]

def register():
    bpy.utils.register_class(JoinByDistance)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
        # you can chnge the shortcut later
        kmi = km.keymap_items.new(JoinByDistance.bl_idname, 'J', 'PRESS')
        addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(JoinByDistance)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
