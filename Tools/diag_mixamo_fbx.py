"""Le o alice_RIGGED.fbx no Blender pra saber a ORIENTACAO real do mesh+armature
e quantos meshes/armatures vieram (braco duplicado = 2 meshes?)."""
import bpy, mathutils
p=r"E:\References\3D\alice_RIGGED.fbx"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=p, automatic_bone_orientation=True)
meshes=[o for o in bpy.data.objects if o.type=='MESH']
arms=[o for o in bpy.data.objects if o.type=='ARMATURE']
print(f"FX meshes={len(meshes)} armatures={len(arms)}")
for m in meshes:
    bb=[m.matrix_world @ mathutils.Vector(c) for c in m.bound_box]
    xs=[v.x for v in bb]; ys=[v.y for v in bb]; zs=[v.z for v in bb]
    print(f"FX mesh '{m.name}' verts={len(m.data.vertices)} dims=(x={max(xs)-min(xs):.2f}, y={max(ys)-min(ys):.2f}, z={max(zs)-min(zs):.2f})")
    print(f"FX   rot_euler=({m.rotation_euler.x:.2f},{m.rotation_euler.y:.2f},{m.rotation_euler.z:.2f})")
    print(f"FX   scale=({m.scale.x:.3f},{m.scale.y:.3f},{m.scale.z:.3f})")
for a in arms:
    print(f"FX armature '{a.name}' bones={len(a.data.bones)} dim_z={a.dimensions.z:.3f}")
    print(f"FX   rot_euler=({a.rotation_euler.x:.2f},{a.rotation_euler.y:.2f},{a.rotation_euler.z:.2f})")
    # bones-chave
    for bn in ("mixamorig:Hips","mixamorig:Head","mixamorig:LeftHand","mixamorig:RightHand","mixamorig:LeftFoot"):
        b=a.data.bones.get(bn)
        if b: print(f"FX   {bn} head=({b.head_local.x:.2f},{b.head_local.y:.2f},{b.head_local.z:.2f})")
print("FX DONE")
