"""Inspeciona E:\References\3D\alice_mixamo.fbx (79k verts) — ja tem rig/pesos?
Se SIM = usa direto. Se NAO (so mesh) = e a Alice ja reduzida, mando pro Mixamo.
Tambem checa alice_mixamo.fbm (texturas)."""
import bpy, os

p = r"E:\References\3D\alice_mixamo.fbx"
print("AM exists=%s size=%dKB" % (os.path.exists(p), os.path.getsize(p)//1024))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=p, automatic_bone_orientation=True)
meshes=[o for o in bpy.data.objects if o.type=='MESH']
arms=[o for o in bpy.data.objects if o.type=='ARMATURE']
print("AM meshes=%d armatures=%d" % (len(meshes), len(arms)))
for m in meshes:
    # influencias
    maxinf=0; total=0; n=0
    step=max(1,len(m.data.vertices)//3000)
    for i in range(0,len(m.data.vertices),step):
        infl=sum(1 for g in m.data.vertices[i].groups if g.weight>0.001)
        maxinf=max(maxinf,infl); total+=infl; n+=1
    avg=total/n if n else 0
    mats=[mt.name for mt in m.data.materials if mt]
    tex=[]
    for mt in m.data.materials:
        if mt and mt.use_nodes:
            for nd in mt.node_tree.nodes:
                if nd.type=='TEX_IMAGE' and nd.image: tex.append(nd.image.name)
    print("AM mesh '%s' verts=%d vgroups=%d maxInfl=%d avgInfl=%.2f mats=%s tex=%s" % (
        m.name, len(m.data.vertices), len(m.vertex_groups), maxinf, avg, mats, tex))
for a in arms:
    print("AM armature '%s' bones=%d" % (a.name, len(a.data.bones)))
print("AM DONE")
