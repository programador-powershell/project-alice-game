"""Export the Alice mesh (GLB) to a Mixamo-ready FBX (mesh only, textures embedded)."""
import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"E:\temp_glb_import\SM_Alice_3D.glb")

m = next((o for o in bpy.data.objects if o.type == 'MESH'), None)
if not m:
    print("ALICEFBX ERROR: no mesh"); raise SystemExit

for o in bpy.data.objects:
    o.select_set(o.type == 'MESH')
bpy.context.view_layer.objects.active = m
try:
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
except Exception as e:
    print("ALICEFBX apply:", e)

bpy.ops.export_scene.fbx(
    filepath=r"E:\model\Alice_for_mixamo.fbx",
    use_selection=True, object_types={'MESH'},
    path_mode='COPY', embed_textures=True, add_leaf_bones=False, bake_anim=False)
print("ALICEFBX DONE verts=%d" % len(m.data.vertices))
