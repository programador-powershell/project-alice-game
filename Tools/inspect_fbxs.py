"""Inspeciona varios FBX usando Blender headless: lista mesh/armature/anim de cada."""
import bpy, sys, os

fbx_dir = r"E:\References\3D"
candidates = ["SK_Alice.fbx","SK_AliceDress.fbx","Alice-T-Pose.fbx","alice_mixamo.fbx"]

print("==== FBX INSPECT ====")
for name in candidates:
    p = os.path.join(fbx_dir, name)
    if not os.path.exists(p):
        print(f"[{name}] MISSING"); continue
    bpy.ops.wm.read_homefile(use_empty=True)
    try:
        bpy.ops.import_scene.fbx(filepath=p, automatic_bone_orientation=True)
    except Exception as e:
        print(f"[{name}] IMPORT ERR: {e}"); continue
    meshes = [o for o in bpy.data.objects if o.type=='MESH']
    armatures = [o for o in bpy.data.objects if o.type=='ARMATURE']
    actions = list(bpy.data.actions)
    bytes_kb = int(os.path.getsize(p)/1024)
    print(f"[{name:30s}] {bytes_kb:6d}KB  meshes={len(meshes)} armatures={len(armatures)} actions={len(actions)}")
    for m in meshes:
        verts = len(m.data.vertices)
        # checa skin weights: tem vertex groups?
        vg = len(m.vertex_groups)
        # quantos verts tem weight em pelo menos 1 vg?
        skinned = 0
        for v in m.data.vertices:
            if v.groups: skinned += 1
        skin_pct = 100*skinned/max(verts,1)
        print(f"   mesh '{m.name}'  verts={verts}  vgroups={vg}  skinned={skin_pct:.0f}%")
    for a in armatures:
        print(f"   armature '{a.name}' bones={len(a.data.bones)}")
print("==== END ====")
