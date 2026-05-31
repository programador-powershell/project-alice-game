import bpy
import mathutils

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"E:\temp_glb_import\SM_Alice_3D.glb")

meshes = [o for o in bpy.data.objects if o.type == 'MESH']
arms = [o for o in bpy.data.objects if o.type == 'ARMATURE']
print("ALICE_INSPECT meshes=%d armatures=%d" % (len(meshes), len(arms)))

for o in meshes:
    me = o.data
    bb = [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    xs = [v.x for v in bb]; ys = [v.y for v in bb]; zs = [v.z for v in bb]
    print("ALICE_INSPECT obj=%s verts=%d polys=%d materials=%d" % (o.name, len(me.vertices), len(me.polygons), len(o.material_slots)))
    print("ALICE_INSPECT  bounds dx=%.3f dy=%.3f dz=%.3f (W=%.3f D=%.3f H=%.3f)" % (
        min(xs), min(ys), min(zs), max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs)))

print("ALICE_INSPECT DONE")
