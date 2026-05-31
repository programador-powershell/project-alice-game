"""DO ZERO — Rig da Alice protagonista:
  mesh   = alice-vestido.glb (922k verts + textura PBR)
  esqueleto doador = Alice-T-Pose.fbx (mixamorig 65 bones, oficial da Alice)
  metodo = auto-weight (parent ARMATURE_AUTO)
Saida = E:\model\SK_Alice_Vestido.fbx (mesh + armature + pesos + textura embutida)
"""
import bpy, mathutils
P = lambda s: print("RIGA " + s)

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. mesh vestido (com textura)
bpy.ops.import_scene.gltf(filepath=r"E:\References\3D\alice-vestido.glb")
alice = next((o for o in bpy.data.objects if o.type=='MESH'), None)
if not alice: P("ERRO sem mesh"); raise SystemExit
alice.name = "Alice_Vestido"
bpy.ops.object.select_all(action='DESELECT')
alice.select_set(True); bpy.context.view_layer.objects.active = alice
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
P("vestido verts=%d mats=%d" % (len(alice.data.vertices), len(alice.data.materials)))

def bb(o):
    pts=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    xs=[p.x for p in pts]; ys=[p.y for p in pts]; zs=[p.z for p in pts]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
axmin,axmax,aymin,aymax,azmin,azmax = bb(alice)
ah = azmax-azmin
P("alice altura=%.3f largura=%.3f" % (ah, axmax-axmin))

# 2. esqueleto oficial da Alice (so armature)
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\Alice-T-Pose.fbx", automatic_bone_orientation=True)
arm = next((o for o in bpy.data.objects if o.type=='ARMATURE'), None)
if not arm: P("ERRO sem armature"); raise SystemExit
P("armature bones=%d dim_z=%.3f" % (len(arm.data.bones), arm.dimensions.z))

# 3. escala armature pra altura da Alice
eh = arm.dimensions.z
if eh>0.001 and ah>0.001:
    sf = ah/eh
    arm.scale=(sf,sf,sf)
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True); bpy.context.view_layer.objects.active=arm
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    P("armature escalada sf=%.3f" % sf)
bpy.context.view_layer.update()

# 4. posiciona armature centrada nos pes da Alice
arm.location = ((axmin+axmax)*0.5, (aymin+aymax)*0.5, azmin)
bpy.context.view_layer.update()
P("armature posicionada")

# 5. auto-weight (pode demorar com 922k verts)
bpy.ops.object.select_all(action='DESELECT')
alice.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active = arm
try:
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    P("auto-weight OK vgroups=%d" % len(alice.vertex_groups))
except Exception as e:
    P("auto-weight FAIL %s" % e); raise SystemExit

# 6. export FBX com textura
for o in bpy.data.objects:
    o.select_set(o.type in ('ARMATURE','MESH'))
bpy.ops.export_scene.fbx(
    filepath=r"E:\model\SK_Alice_Vestido.fbx",
    use_selection=True, object_types={'ARMATURE','MESH'},
    add_leaf_bones=False, bake_anim=False,
    path_mode='COPY', embed_textures=True, mesh_smooth_type='FACE')
P("EXPORT DONE -> E:\\model\\SK_Alice_Vestido.fbx vgroups=%d" % len(alice.vertex_groups))
