import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)
try:
    bpy.ops.import_scene.fbx(filepath=r"E:\model\Y Bot.fbx")
except Exception as e:
    print("YBOT IMPORT ERROR: %s" % e)

arms = [o for o in bpy.data.objects if o.type == 'ARMATURE']
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
print("YBOT meshes=%d armatures=%d actions=%d" % (len(meshes), len(arms), len(bpy.data.actions)))
for a in arms:
    print("YBOT armature=%s bones=%d" % (a.name, len(a.data.bones)))
for m in meshes:
    print("YBOT mesh=%s verts=%d" % (m.name, len(m.data.vertices)))
for ac in bpy.data.actions:
    try:
        print("YBOT action=%s frames=%.0f-%.0f" % (ac.name, ac.frame_range[0], ac.frame_range[1]))
    except Exception:
        print("YBOT action=%s" % ac.name)
print("YBOT DONE")
