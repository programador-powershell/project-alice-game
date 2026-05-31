"""Le no Blender o numero REAL de influencias por vertice de cada modelo.
Decide se o problema e o GLB da Alice (denso, scan) vs FBX mixamo dos bosses."""
import bpy, os

def check(path, label):
    if not os.path.exists(path):
        print(f"INF [{label}] MISSING"); return
    bpy.ops.wm.read_factory_settings(use_empty=True)
    try:
        if path.endswith(".glb"):
            bpy.ops.import_scene.gltf(filepath=path)
        else:
            bpy.ops.import_scene.fbx(filepath=path, automatic_bone_orientation=True)
    except Exception as e:
        print(f"INF [{label}] ERR {e}"); return
    m = next((o for o in bpy.data.objects if o.type=='MESH'), None)
    if not m:
        print(f"INF [{label}] sem mesh"); return
    # conta influencias por vertice (numero de grupos com peso>0)
    counts = {}
    sample = min(len(m.data.vertices), 5000)
    step = max(1, len(m.data.vertices)//sample)
    maxinf = 0; total=0; n=0
    for i in range(0, len(m.data.vertices), step):
        v = m.data.vertices[i]
        infl = sum(1 for g in v.groups if g.weight > 0.001)
        maxinf = max(maxinf, infl); total += infl; n+=1
        counts[infl] = counts.get(infl,0)+1
    avg = total/n if n else 0
    print(f"INF [{label:22s}] verts={len(m.data.vertices)} vgroups={len(m.vertex_groups)} maxInfl={maxinf} avgInfl={avg:.2f} dist={dict(sorted(counts.items()))}")

check(r"E:\References\3D\alice-vestido.glb", "alice-vestido.glb")
check(r"E:\References\3D\coelho-vestidoT-Pose.fbx", "coelho-vestidoTPose")
check(r"E:\References\3D\chapeleiro-T-Pose.fbx", "chapeleiro-TPose")
check(r"E:\model\SK_Alice_V2.fbx", "SK_Alice_V2 (rig meu)")
print("INF DONE")
