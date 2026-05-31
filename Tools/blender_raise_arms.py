"""
Attempt to raise Alice's arms to a T-pose (so a rig can separate arms from the dress),
then RENDER front+side clay so we can verify before using it. Exports Alice_Tpose.fbx.
Heuristic vertex rotation — verify the render before trusting it.
"""
import bpy
import math
import mathutils

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"E:\temp_glb_import\SM_Alice_3D.glb")
alice = next((o for o in bpy.data.objects if o.type == 'MESH'), None)
if not alice:
    print("RAISE ERROR no mesh"); raise SystemExit
alice.name = "Alice"

# apply transforms so local == world
bpy.ops.object.select_all(action='DESELECT')
alice.select_set(True)
bpy.context.view_layer.objects.active = alice
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

me = alice.data
xs = [v.co.x for v in me.vertices]
ys = [v.co.y for v in me.vertices]
zs = [v.co.z for v in me.vertices]
cx = (min(xs) + max(xs)) * 0.5
zmin, zmax = min(zs), max(zs)
H = zmax - zmin
W = max(xs) - min(xs)

shoulderZ = zmin + 0.78 * H
hipZ = zmin + 0.45 * H

# Estimate torso half-width at shoulder band (verts near shoulderZ, to know where torso ends)
band = [abs(v.co.x - cx) for v in me.vertices if shoulderZ - 0.06 * H < v.co.z < shoulderZ + 0.04 * H]
torso_half = (sorted(band)[int(len(band) * 0.5)] if band else 0.12 * W)

raised = 0
for v in me.vertices:
    p = v.co
    side = 1.0 if p.x > cx else -1.0
    ax = abs(p.x - cx)
    # arm region: hip..shoulder height, lateral beyond torso but not the far dress hem
    if hipZ < p.z < shoulderZ + 0.06 * H and torso_half * 0.85 < ax < torso_half + 0.30 * W:
        pivotX = cx + side * torso_half
        pivotZ = shoulderZ
        dx = p.x - pivotX
        dz = p.z - pivotZ
        ang = side * math.radians(72.0)  # swing the hanging arm up to horizontal
        ndx = dx * math.cos(ang) - dz * math.sin(ang)
        ndz = dx * math.sin(ang) + dz * math.cos(ang)
        v.co.x = pivotX + ndx
        v.co.z = pivotZ + ndz
        raised += 1
me.update()
print("RAISE raised %d verts torso_half=%.3f H=%.3f" % (raised, torso_half, H))

# --- render front clay to verify ---
import os
os.makedirs(r"E:\Alice\_PREVIEWS", exist_ok=True)
# camera (front, ortho)
cam_data = bpy.data.cameras.new("Cam"); cam_data.type = 'ORTHO'; cam_data.ortho_scale = H * 1.4
cam = bpy.data.objects.new("Cam", cam_data); bpy.context.collection.objects.link(cam)
cx2 = (min(v.co.x for v in me.vertices) + max(v.co.x for v in me.vertices)) * 0.5
cam.location = (cx2, -H * 2.0, zmin + H * 0.5)
cam.rotation_euler = (math.radians(90), 0, 0)
bpy.context.scene.camera = cam
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sc.render.resolution_x = 600; sc.render.resolution_y = 800
sc.render.filepath = r"E:\Alice\_PREVIEWS\alice_tpose.png"
try:
    sc.display.shading.light = 'STUDIO'
    sc.display.shading.show_cavity = True
except Exception:
    pass
bpy.ops.render.render(write_still=True)
print("RAISE rendered")

# export T-pose mesh for Mixamo / re-rig
bpy.ops.object.select_all(action='DESELECT')
alice.select_set(True)
bpy.ops.export_scene.fbx(filepath=r"E:\model\Alice_Tpose.fbx", use_selection=True,
                         object_types={'MESH'}, path_mode='COPY', embed_textures=True,
                         add_leaf_bones=False, bake_anim=False)
print("RAISE DONE")
