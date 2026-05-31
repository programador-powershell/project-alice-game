import bpy, mathutils, os, math
BASE = r"E:\References\3D"; OUT = r"E:\Alice\_PREVIEWS"; LOG = r"E:\Alice\wpn_info.txt"
os.makedirs(OUT, exist_ok=True)
open(LOG, "w", encoding="utf-8").write("")
def wlog(s):
    with open(LOG, "a", encoding="utf-8") as f: f.write(s + "\n")
def wbb(o):
    return [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]

for w in ["espadao", "cajado", "punhal", "odachi", "faca", "adaga", "foice"]:
    p = os.path.join(BASE, w + ".glb")
    if not os.path.exists(p):
        wlog(w + " MISSING"); continue
    bpy.ops.wm.read_homefile(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=p)
    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    wlog("=== %s : objs=%d ===" % (w, len(meshes)))
    for m in meshes:
        wlog("  obj '%s' dims=%s verts=%d" % (m.name, [round(d, 3) for d in m.dimensions], len(m.data.vertices)))
    allbb = []
    for m in meshes: allbb += wbb(m)
    if not allbb: continue
    ctr = sum(allbb, mathutils.Vector()) / len(allbb)
    size = max((max(v[i] for v in allbb) - min(v[i] for v in allbb)) for i in range(3)) or 1.0
    cd = bpy.data.cameras.new("C"); cam = bpy.data.objects.new("C", cd); bpy.context.collection.objects.link(cam)
    cam.location = ctr + mathutils.Vector((size * 1.6, -size * 2.0, size * 0.5))
    cam.rotation_euler = (ctr - cam.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    ld = bpy.data.lights.new("S", 'SUN'); ld.energy = 4.0
    lo = bpy.data.objects.new("S", ld); bpy.context.collection.objects.link(lo); lo.rotation_euler = (math.radians(50), 0, math.radians(40))
    sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'
    sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'SINGLE'
    sc.render.resolution_x = 500; sc.render.resolution_y = 600
    sc.render.filepath = os.path.join(OUT, "wpn_%s.png" % w)
    bpy.ops.render.render(write_still=True)
wlog("DONE")
