import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)
try:
    bpy.ops.import_scene.fbx(filepath=r"E:\model\Eve.fbx")
except Exception as e:
    print("EVE IMPORT ERROR: %s" % e)

arms = [o for o in bpy.data.objects if o.type == 'ARMATURE']
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
print("EVE meshes=%d armatures=%d actions=%d" % (len(meshes), len(arms), len(bpy.data.actions)))
for a in arms:
    print("EVE armature=%s bones=%d" % (a.name, len(a.data.bones)))
    names = [b.name for b in a.data.bones][:12]
    print("EVE bones_sample=%s" % names)
for m in meshes:
    print("EVE mesh=%s verts=%d materials=%d" % (m.name, len(m.data.vertices), len(m.material_slots)))
for ac in bpy.data.actions:
    try:
        print("EVE action=%s frames=%.0f-%.0f" % (ac.name, ac.frame_range[0], ac.frame_range[1]))
    except Exception:
        print("EVE action=%s" % ac.name)
print("EVE DONE")
