"""
Rig the Alice mesh (her art) to Eve's mixamorig skeleton (donor) — scale FIXED.
Scales the armature to fit Alice, auto-weights, exports SK_Alice.fbx. Imported onto
SK_EveM_Skeleton in UE, the existing Mixamo clips reuse on Alice. Dress deforms a bit
(no skirt bones) — refine/cloth later.
"""
import bpy
import mathutils

bpy.ops.wm.read_factory_settings(use_empty=True)

bpy.ops.import_scene.gltf(filepath=r"E:\temp_glb_import\SM_Alice_3D.glb")
alice = next((o for o in bpy.data.objects if o.type == 'MESH'), None)
if not alice:
    print("RIGALICE2 ERROR no alice"); raise SystemExit
alice.name = "Alice"

bpy.ops.import_scene.fbx(filepath=r"E:\model\Eve.fbx")
arm = next((o for o in bpy.data.objects if o.type == 'ARMATURE'), None)
eve_meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.name != "Alice"]
if not arm:
    print("RIGALICE2 ERROR no armature"); raise SystemExit


def bb(o):
    pts = [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    zs = [p.z for p in pts]; xs = [p.x for p in pts]; ys = [p.y for p in pts]
    return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)


axmin, axmax, aymin, aymax, azmin, azmax = bb(alice)
ah = azmax - azmin
# armature size: use Eve mesh height if present, else armature dimensions
if eve_meshes:
    _, _, _, _, ezmin, ezmax = bb(eve_meshes[0])
    eh = ezmax - ezmin
else:
    eh = arm.dimensions.z

# scale the ARMATURE up/down to Alice's height (so bones fill Alice's body), then apply
if eh > 0.001 and ah > 0.001:
    sf = ah / eh
    arm.scale = (sf, sf, sf)
    bpy.ops.object.select_all(action='DESELECT')
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
bpy.context.view_layer.update()

# place armature: base at Alice feet, centered on Alice XY
arm.location = ((axmin + axmax) * 0.5, (aymin + aymax) * 0.5, azmin)
bpy.context.view_layer.update()

# remove Eve meshes (keep armature + Alice)
for o in eve_meshes:
    bpy.data.objects.remove(o, do_unlink=True)

# automatic-weight bind
bpy.ops.object.select_all(action='DESELECT')
alice.select_set(True)
arm.select_set(True)
bpy.context.view_layer.objects.active = arm
try:
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    print("RIGALICE2 auto-weight ok")
except Exception as e:
    print("RIGALICE2 auto-weight FAIL", e)

for o in bpy.data.objects:
    o.select_set(o.type in ('ARMATURE', 'MESH'))
bpy.ops.export_scene.fbx(filepath=r"E:\model\SK_Alice.fbx", use_selection=True,
                         add_leaf_bones=False, bake_anim=False, object_types={'ARMATURE', 'MESH'})
print("RIGALICE2 DONE ah=%.3f eh=%.3f sf=%.3f" % (ah, eh, (ah / eh) if eh > 0.001 else 0))
