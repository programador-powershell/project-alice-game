"""Inspeciona alice_RIGGED.fbx: armature, bones, mesh, pesos (maxInfl), material."""
import bpy, os
p=r"E:\References\3D\alice_RIGGED.fbx"
print("IR size=%dKB" % (os.path.getsize(p)//1024))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=p, automatic_bone_orientation=True)
meshes=[o for o in bpy.data.objects if o.type=='MESH']
arms=[o for o in bpy.data.objects if o.type=='ARMATURE']
print("IR meshes=%d armatures=%d" % (len(meshes), len(arms)))
for a in arms:
    bn=[b.name for b in a.data.bones]
    print("IR armature '%s' bones=%d sample=%s" % (a.name, len(bn), bn[:5]))
for m in meshes:
    maxinf=0;tot=0;n=0
    step=max(1,len(m.data.vertices)//3000)
    for i in range(0,len(m.data.vertices),step):
        infl=sum(1 for g in m.data.vertices[i].groups if g.weight>0.001)
        maxinf=max(maxinf,infl);tot+=infl;n+=1
    avg=tot/n if n else 0
    mats=[mt.name for mt in m.data.materials if mt]
    print("IR mesh '%s' verts=%d vgroups=%d maxInfl=%d avg=%.2f mats=%s" % (
        m.name,len(m.data.vertices),len(m.vertex_groups),maxinf,avg,mats))
print("IR DONE")
