"""Rig da Alice usando a versao JA REDUZIDA (alice_mixamo.fbx, 79k verts):
  mesh   = alice_mixamo.fbx (79k, mesma textura PBR, SEM rig)
  rig     = Alice-T-Pose.fbx (49 bones mixamorig)
  metodo = auto-weight + limit 4 + normalize
VALIDA influencias ANTES de exportar (no proprio Blender) — se avg>1 exporta, senao avisa.
"""
import bpy, mathutils
P = lambda s: print("R79 " + s)

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. mesh reduzido (com textura)
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\alice_mixamo.fbx", automatic_bone_orientation=True)
alice = next((o for o in bpy.data.objects if o.type=='MESH'), None)
alice.name = "Alice"
bpy.ops.object.select_all(action='DESELECT')
alice.select_set(True); bpy.context.view_layer.objects.active=alice
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
P("mesh verts=%d mats=%d" % (len(alice.data.vertices), len(alice.data.materials)))

def bb(o):
    pts=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    xs=[p.x for p in pts]; ys=[p.y for p in pts]; zs=[p.z for p in pts]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
axmin,axmax,aymin,aymax,azmin,azmax = bb(alice)
ah=azmax-azmin
P("alice altura=%.3f" % ah)

# 2. rig Alice-T-Pose
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\Alice-T-Pose.fbx", automatic_bone_orientation=True)
arm = next((o for o in bpy.data.objects if o.type=='ARMATURE'), None)
P("armature bones=%d dim_z=%.3f" % (len(arm.data.bones), arm.dimensions.z))

eh = arm.dimensions.z
if eh>0.001 and ah>0.001:
    sf=ah/eh; arm.scale=(sf,sf,sf)
    bpy.ops.object.select_all(action='DESELECT'); arm.select_set(True)
    bpy.context.view_layer.objects.active=arm
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    P("armature escalada sf=%.3f" % sf)
arm.location=((axmin+axmax)*0.5,(aymin+aymax)*0.5,azmin)
bpy.context.view_layer.update()

# 3. auto-weight
bpy.ops.object.select_all(action='DESELECT')
alice.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active=arm
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
P("auto-weight vgroups=%d" % len(alice.vertex_groups))

# 4. limit 4 + normalize
bpy.ops.object.select_all(action='DESELECT')
alice.select_set(True); bpy.context.view_layer.objects.active=alice
bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
bpy.ops.object.vertex_group_limit_total(limit=4)
bpy.ops.object.vertex_group_normalize_all(lock_active=False)
bpy.ops.object.mode_set(mode='OBJECT')

# 5. VALIDA influencias ANTES de exportar
maxinf=0; total=0; n=0
step=max(1,len(alice.data.vertices)//5000)
for i in range(0,len(alice.data.vertices),step):
    infl=sum(1 for g in alice.data.vertices[i].groups if g.weight>0.001)
    maxinf=max(maxinf,infl); total+=infl; n+=1
avg=total/n if n else 0
P("VALIDACAO: maxInfl=%d avgInfl=%.2f" % (maxinf, avg))

if avg < 1.0:
    P("ERRO: pesos degenerados (avg<1) — NAO exporto. auto-weight falhou nesta malha.")
    raise SystemExit

# 6. export
for o in bpy.data.objects:
    o.select_set(o.type in ('ARMATURE','MESH'))
bpy.ops.export_scene.fbx(
    filepath=r"E:\model\SK_Alice_79k.fbx",
    use_selection=True, object_types={'ARMATURE','MESH'},
    add_leaf_bones=False, bake_anim=False,
    path_mode='COPY', embed_textures=True, mesh_smooth_type='FACE')
P("EXPORT OK -> E:\\model\\SK_Alice_79k.fbx (avg infl=%.2f)" % avg)
P("R79DONE")
