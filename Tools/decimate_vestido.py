"""Decima alice-vestido.glb (922k verts) -> ~80k, exporta FBX pronto p/ Mixamo.
Mantem textura. Saida: E:\References\3D\alice_vestido_mixamo.fbx
"""
import bpy
P = lambda s: print("DEC " + s)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"E:\References\3D\alice-vestido.glb")
m = next((o for o in bpy.data.objects if o.type=='MESH'), None)
if not m: P("ERRO sem mesh"); raise SystemExit
m.name = "AliceVestido"
v0 = len(m.data.vertices)
P("verts orig=%d mats=%d" % (v0, len(m.data.materials)))

bpy.ops.object.select_all(action='DESELECT')
m.select_set(True); bpy.context.view_layer.objects.active = m
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# alvo ~75k verts (limite Mixamo 150k poly; ratio = alvo/orig)
TARGET = 75000
ratio = min(1.0, TARGET / max(1, v0))
P("decimate ratio=%.4f" % ratio)
dec = m.modifiers.new("Dec", 'DECIMATE')
dec.decimate_type = 'COLLAPSE'
dec.ratio = ratio
bpy.ops.object.modifier_apply(modifier="Dec")
v1 = len(m.data.vertices)
P("verts apos decimate=%d" % v1)

# export FBX mesh-only + textura embed
for o in bpy.data.objects:
    o.select_set(o.type=='MESH')
bpy.ops.export_scene.fbx(
    filepath=r"E:\References\3D\alice_vestido_mixamo.fbx",
    use_selection=True, object_types={'MESH'},
    path_mode='COPY', embed_textures=True,
    add_leaf_bones=False, bake_anim=False, mesh_smooth_type='FACE')
P("EXPORT -> E:\\References\\3D\\alice_vestido_mixamo.fbx verts=%d" % v1)
P("DECDONE")
