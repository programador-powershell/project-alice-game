"""Inspeciona os T-Pose rigados: mesh/armature/verts/vgroups/material.
Descobre quais ja vem prontos (rig+roupa+pesos) vs quais precisam rig."""
import bpy, os

cands = [
    r"E:\References\3D\Alice-T-Pose.fbx",
    r"E:\References\3D\chapeleiro-T-Pose.fbx",
    r"E:\References\3D\coelho-vestidoT-Pose.fbx",
    r"E:\References\3D\Coelho-T-Pose.fbx",
    r"E:\References\3D\Lidia-T-Pose.fbx",
    r"E:\References\3D\cavaleiro-T-Pose.fbx",
    r"E:\References\3D\alice_mixamo.fbx",
]
for p in cands:
    if not os.path.exists(p):
        print(f"TP [{os.path.basename(p)}] MISSING"); continue
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        bpy.ops.import_scene.fbx(filepath=p, automatic_bone_orientation=True)
    except Exception as e:
        print(f"TP [{os.path.basename(p)}] IMPORT_ERR {e}"); continue
    meshes=[o for o in bpy.data.objects if o.type=='MESH']
    arms=[o for o in bpy.data.objects if o.type=='ARMATURE']
    kb=int(os.path.getsize(p)/1024)
    nb = len(arms[0].data.bones) if arms else 0
    tv = sum(len(m.data.vertices) for m in meshes)
    tvg = sum(len(m.vertex_groups) for m in meshes)
    nmat = sum(len(m.data.materials) for m in meshes)
    rigged = "RIGADO+PESOS" if (arms and tvg>0) else ("SO_ANIM/sem_mesh" if not meshes else "MESH_sem_rig")
    print(f"TP [{os.path.basename(p):28s}] {kb:6d}KB mesh={len(meshes)} verts={tv} arm={len(arms)} bones={nb} vgroups={tvg} mats={nmat} => {rigged}")
print("TP DONE")
