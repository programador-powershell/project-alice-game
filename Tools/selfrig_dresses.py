import bpy, mathutils, os, traceback
LOG = r"E:\Alice\dresses_result.txt"
with open(LOG, "w", encoding="utf-8") as f:
    f.write("STARTED\n")
def log(m):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(str(m) + "\n")

EVE = r"E:\model\Eve.fbx"; BASE = r"E:\References\3D"
DRESSES = [
    ("alice-coelho",     "SK_Alice_Coelho",     "acoelho",  "alice_coelho_tex"),
    ("alice-cheshire",   "SK_Alice_Cheshire",   "acheshire","alice_cheshire_tex"),
    ("alice-chapepeiro", "SK_Alice_Chapeleiro", "achap",    "alice_chapeleiro_tex"),
    ("alice-lagarta",    "SK_Alice_Lagarta",    "alagarta", "alice_lagarta_tex"),
    ("alice-rainha",     "SK_Alice_Rainha",     "arainha",  "alice_rainha_tex"),
]
def wbb(o):
    return [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
def ov(active, sel):
    return bpy.context.temp_override(active_object=active, object=active,
                                     selected_objects=sel, selected_editable_objects=sel)

for glb, outn, texp, td in DRESSES:
    try:
        gpath = os.path.join(BASE, glb + ".glb")
        if not os.path.exists(gpath):
            log("MISS " + gpath); continue
        bpy.ops.wm.read_homefile(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=gpath)
        me = next(o for o in bpy.data.objects if o.type == 'MESH'); me.name = "M"
        bpy.context.view_layer.objects.active = me
        dm = me.modifiers.new("d", "DECIMATE"); dm.decimate_type = 'COLLAPSE'
        dm.ratio = min(1.0, 120000.0 / len(me.data.vertices))
        with ov(me, [me]):
            bpy.ops.object.modifier_apply(modifier="d")
        mb = wbb(me); mzmin = min(v.z for v in mb); mh = max(v.z for v in mb) - mzmin
        s = 1.70 / mh; me.scale = (s, s, s)
        with ov(me, [me]):
            bpy.ops.object.transform_apply(scale=True)
        mb = wbb(me); mzmin = min(v.z for v in mb); mh = max(v.z for v in mb) - mzmin
        mcx = sum(v.x for v in mb)/8.0; mcy = sum(v.y for v in mb)/8.0
        before = set(bpy.data.objects)
        bpy.ops.import_scene.fbx(filepath=EVE)
        arm = next(o for o in bpy.data.objects if o not in before and o.type == 'ARMATURE')
        for o in [x for x in bpy.data.objects if x not in before and x.type == 'MESH']:
            bpy.data.objects.remove(o, do_unlink=True)
        ab = wbb(arm); ah = max(v.z for v in ab) - min(v.z for v in ab); sc2 = mh / ah
        arm.scale = (arm.scale[0]*sc2, arm.scale[1]*sc2, arm.scale[2]*sc2)
        bpy.context.view_layer.update()
        ab = wbb(arm); azmin = min(v.z for v in ab); acx = sum(v.x for v in ab)/8.0; acy = sum(v.y for v in ab)/8.0
        arm.location.x += (mcx-acx); arm.location.y += (mcy-acy); arm.location.z += (mzmin-azmin)
        bpy.context.view_layer.update()
        with ov(arm, [me, arm]):
            bpy.ops.object.parent_set(type='ARMATURE_AUTO')
        with ov(arm, [me, arm]):
            bpy.ops.export_scene.fbx(filepath=os.path.join(BASE, outn + ".fbx"), use_selection=True,
                                     object_types={'ARMATURE', 'MESH'}, add_leaf_bones=False,
                                     bake_anim=False, mesh_smooth_type='FACE', path_mode='COPY')
        tdp = os.path.join(BASE, td); os.makedirs(tdp, exist_ok=True)
        for i in bpy.data.images:
            if i.size[0] > 0 and 'texture_pbr' in i.name.lower():
                n = i.name.lower(); key = 'normal' if 'normal' in n else ('mr' if ('metallic' in n or 'roughness' in n) else 'base')
                i.filepath_raw = os.path.join(tdp, "%s_%s.png" % (texp, key)); i.file_format = 'PNG'; i.save()
        log("DONE %s verts=%d" % (outn, len(me.data.vertices)))
    except Exception as e:
        log("FAIL %s :: %r" % (outn, e))
        log(traceback.format_exc())
log("ALL_DONE")
