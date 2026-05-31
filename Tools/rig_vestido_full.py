"""RIG COMPLETO: alice-vestido.glb -> mixamorig (doador Eve.fbx) -> auto-weight -> FBX com textura.
Saida: E:\model\SK_AliceVestido.fbx (mesh + armature + pesos + textura embutida).
"""
import bpy, mathutils

LOG = lambda s: print("RIGV " + s)

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. importa o vestido (mesh + material + textura embutida)
bpy.ops.import_scene.gltf(filepath=r"E:\References\3D\alice-vestido.glb")
alice = next((o for o in bpy.data.objects if o.type=='MESH'), None)
if not alice: LOG("ERRO sem mesh vestido"); raise SystemExit
alice.name = "AliceVestido"
LOG("vestido verts=%d mats=%d" % (len(alice.data.vertices), len(alice.data.materials)))

# aplica transforms do mesh
bpy.ops.object.select_all(action='DESELECT')
alice.select_set(True); bpy.context.view_layer.objects.active = alice
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

def bb(o):
    pts=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    xs=[p.x for p in pts]; ys=[p.y for p in pts]; zs=[p.z for p in pts]
    return min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)

axmin,axmax,aymin,aymax,azmin,azmax = bb(alice)
ah = azmax-azmin
LOG("alice altura=%.3f" % ah)

# 2. importa Eve (doador de armature mixamorig)
bpy.ops.import_scene.fbx(filepath=r"E:\model\Eve.fbx")
arm = next((o for o in bpy.data.objects if o.type=='ARMATURE'), None)
eve_meshes = [o for o in bpy.data.objects if o.type=='MESH' and o.name!="AliceVestido"]
if not arm: LOG("ERRO sem armature Eve"); raise SystemExit
LOG("armature bones=%d" % len(arm.data.bones))

# altura da Eve (mesh ou armature)
if eve_meshes:
    _,_,_,_,ezmin,ezmax = bb(eve_meshes[0]); eh = ezmax-ezmin
else:
    eh = arm.dimensions.z
LOG("eve altura=%.3f" % eh)

# 3. escala armature pra altura da Alice
if eh>0.001 and ah>0.001:
    sf = ah/eh
    arm.scale=(sf,sf,sf)
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True); bpy.context.view_layer.objects.active=arm
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    LOG("armature escalada sf=%.3f" % sf)
bpy.context.view_layer.update()

# 4. posiciona armature: base nos pes da Alice, centrada
arm.location = ((axmin+axmax)*0.5, (aymin+aymax)*0.5, azmin)
bpy.context.view_layer.update()

# remove meshes da Eve (fica so armature + Alice vestido)
for o in eve_meshes:
    bpy.data.objects.remove(o, do_unlink=True)

# 5. auto-weight bind (pode demorar com 121k verts)
bpy.ops.object.select_all(action='DESELECT')
alice.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active = arm
try:
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    LOG("auto-weight OK vgroups=%d" % len(alice.vertex_groups))
except Exception as e:
    LOG("auto-weight FAIL %s" % e); raise SystemExit

# 6. export FBX com textura embutida
for o in bpy.data.objects:
    o.select_set(o.type in ('ARMATURE','MESH'))
bpy.ops.export_scene.fbx(
    filepath=r"E:\model\SK_AliceVestido.fbx",
    use_selection=True, object_types={'ARMATURE','MESH'},
    add_leaf_bones=False, bake_anim=False,
    path_mode='COPY', embed_textures=True,
    mesh_smooth_type='FACE')
LOG("EXPORT DONE -> E:\\model\\SK_AliceVestido.fbx")
LOG("ALLDONE ah=%.3f eh=%.3f vgroups=%d" % (ah, eh, len(alice.vertex_groups)))
