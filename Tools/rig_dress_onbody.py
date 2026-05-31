"""Riga o vestido no MESMO armature do corpo Mixamo (alice_RIGGED).
Garante mesmo skeleton -> Leader Pose no UE funciona.
1. importa alice_RIGGED (corpo+armature)
2. importa vestido decimado
3. parenta vestido ao armature do corpo (auto-weight)
4. exporta alice_vestido_rigged.fbx (so vestido + armature)
"""
import bpy, mathutils
P = lambda s: print("RD " + s)

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. corpo rigado (tem armature mixamo)
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\alice_RIGGED.fbx", automatic_bone_orientation=True)
arm = next((o for o in bpy.data.objects if o.type=='ARMATURE'), None)
body = next((o for o in bpy.data.objects if o.type=='MESH'), None)
if not arm: P("ERRO sem armature corpo"); raise SystemExit
P("corpo armature bones=%d" % len(arm.data.bones))
# guarda dims do corpo p/ alinhar vestido
def bb(o):
    pts=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    zs=[p.z for p in pts]; return min(zs),max(zs)
bz0,bz1=bb(body); bh=bz1-bz0
P("corpo altura=%.3f" % bh)

# 2. vestido decimado
bpy.ops.import_scene.gltf(filepath=r"E:\References\3D\alice-vestido.glb")
dress=[o for o in bpy.data.objects if o.type=='MESH' and o!=body]
dress=dress[0] if dress else None
if not dress: P("ERRO sem vestido"); raise SystemExit
dress.name="AliceDress"
bpy.ops.object.select_all(action='DESELECT')
dress.select_set(True); bpy.context.view_layer.objects.active=dress
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
# decima vestido p/ ~120k tris
me=dress.data; me.calc_loop_triangles()
t0=len(me.loop_triangles)
d=dress.modifiers.new("Dec",'DECIMATE'); d.ratio=min(1.0,120000/max(1,t0))
bpy.ops.object.modifier_apply(modifier="Dec")
P("vestido decimado tris=%d->%d" % (t0, len(dress.data.loop_triangles)))

# alinha altura vestido ao corpo
dz0,dz1=bb(dress); dh=dz1-dz0
if dh>0.01:
    sf=bh/dh; dress.scale=(sf,sf,sf)
    bpy.ops.object.select_all(action='DESELECT'); dress.select_set(True)
    bpy.context.view_layer.objects.active=dress
    bpy.ops.object.transform_apply(scale=True)
    P("vestido escalado sf=%.3f" % sf)
# realinha base
dz0,dz1=bb(dress); dress.location.z += (bz0-dz0);
bpy.context.view_layer.update()

# 3. parenta vestido ao armature do corpo (auto-weight)
bpy.ops.object.select_all(action='DESELECT')
dress.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active=arm
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
P("vestido auto-weight vgroups=%d" % len(dress.vertex_groups))

# 4. exporta SO vestido + armature
bpy.ops.object.select_all(action='DESELECT')
dress.select_set(True); arm.select_set(True)
bpy.ops.export_scene.fbx(filepath=r"E:\References\3D\alice_vestido_rigged.fbx",
    use_selection=True, object_types={'ARMATURE','MESH'},
    add_leaf_bones=False, bake_anim=False, path_mode='COPY', embed_textures=True,
    mesh_smooth_type='FACE')
P("EXPORT vestido_rigged vgroups=%d" % len(dress.vertex_groups))
P("RDDONE")
