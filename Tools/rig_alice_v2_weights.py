"""Re-rig Alice com pesos MULTI-influencia (4 por vertice).
Problema anterior: MaxBoneInfluences=1 (estatua).
Fix: apos auto-weight, limita a 4 influencias + normaliza + export FBX preservando.
mesh = alice-vestido.glb, rig = Alice-T-Pose (49 bones mixamorig).
"""
import bpy, mathutils
P = lambda s: print("RW " + s)

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. vestido
bpy.ops.import_scene.gltf(filepath=r"E:\References\3D\alice-vestido.glb")
alice = next((o for o in bpy.data.objects if o.type=='MESH'), None)
alice.name = "Alice"
bpy.ops.object.select_all(action='DESELECT')
alice.select_set(True); bpy.context.view_layer.objects.active=alice
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
P("vestido verts=%d" % len(alice.data.vertices))

def bb(o):
    pts=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    xs=[p.x for p in pts]; ys=[p.y for p in pts]; zs=[p.z for p in pts]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
axmin,axmax,aymin,aymax,azmin,azmax = bb(alice)
ah=azmax-azmin

# 2. rig Alice-T-Pose
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\Alice-T-Pose.fbx", automatic_bone_orientation=True)
arm = next((o for o in bpy.data.objects if o.type=='ARMATURE'), None)
P("armature bones=%d" % len(arm.data.bones))

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

# 4. LIMITA a 4 influencias + normaliza (corrige o problema de export)
bpy.ops.object.select_all(action='DESELECT')
alice.select_set(True); bpy.context.view_layer.objects.active=alice
bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
try:
    bpy.ops.object.vertex_group_limit_total(limit=4)
    P("limit_total=4 OK")
except Exception as e:
    P("limit err %s" % e)
try:
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)
    P("normalize_all OK")
except Exception as e:
    P("norm err %s" % e)
bpy.ops.object.mode_set(mode='OBJECT')

# 5. export FBX (FBX suporta ate ilimitadas; UE limita no import)
for o in bpy.data.objects:
    o.select_set(o.type in ('ARMATURE','MESH'))
bpy.ops.export_scene.fbx(
    filepath=r"E:\model\SK_Alice_V2.fbx",
    use_selection=True, object_types={'ARMATURE','MESH'},
    add_leaf_bones=False, bake_anim=False,
    path_mode='COPY', embed_textures=True, mesh_smooth_type='FACE',
    use_armature_deform_only=False)
P("EXPORT DONE -> E:\\model\\SK_Alice_V2.fbx")
