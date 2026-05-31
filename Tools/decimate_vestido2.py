"""Decima alice-vestido.glb mais agressivo p/ caber FOLGADO no Mixamo (<150k tris).
Conta TRIS, mira ~120k tris. Saida: alice_vestido_mixamo.fbx
"""
import bpy
P = lambda s: print("D2 " + s)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"E:\References\3D\alice-vestido.glb")
m = next((o for o in bpy.data.objects if o.type=='MESH'), None)
m.name="AliceVestido"
bpy.ops.object.select_all(action='DESELECT')
m.select_set(True); bpy.context.view_layer.objects.active=m
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# conta tris reais
me=m.data
me.calc_loop_triangles()
tris0=len(me.loop_triangles)
P("tris orig=%d verts=%d" % (tris0, len(me.vertices)))

TARGET_TRIS=120000
ratio=min(1.0, TARGET_TRIS/max(1,tris0))
P("ratio=%.4f (mira %d tris)" % (ratio, TARGET_TRIS))
d=m.modifiers.new("Dec",'DECIMATE'); d.decimate_type='COLLAPSE'; d.ratio=ratio
bpy.ops.object.modifier_apply(modifier="Dec")
me=m.data; me.calc_loop_triangles()
P("apos: tris=%d verts=%d" % (len(me.loop_triangles), len(me.vertices)))

for o in bpy.data.objects: o.select_set(o.type=='MESH')
bpy.ops.export_scene.fbx(filepath=r"E:\References\3D\alice_vestido_mixamo.fbx",
    use_selection=True, object_types={'MESH'}, path_mode='COPY', embed_textures=True,
    add_leaf_bones=False, bake_anim=False, mesh_smooth_type='FACE')
P("EXPORT tris=%d verts=%d" % (len(me.loop_triangles), len(me.vertices)))
P("D2DONE")
