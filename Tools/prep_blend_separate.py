"""Prepara .blend com alice-vestido pronto pra voce separar corpo/vestido manualmente."""
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=r"E:\References\3D\alice-vestido.glb")
m=next(o for o in bpy.data.objects if o.type=='MESH')
m.name="Alice_Full"
# decimar primeiro p/ ficar editavel (922k -> 120k)
bpy.ops.object.select_all(action='DESELECT')
m.select_set(True); bpy.context.view_layer.objects.active=m
d=m.modifiers.new("D",'DECIMATE'); d.decimate_type='COLLAPSE'
me=m.data; me.calc_loop_triangles()
d.ratio=min(1.0, 120000/max(1,len(me.loop_triangles)))
bpy.ops.object.modifier_apply(modifier="D")
print(f"PREP decimado tris={len(m.data.loop_triangles)}")
# salva .blend
bpy.ops.wm.save_as_mainfile(filepath=r"E:\References\3D\alice_para_separar.blend")
print("PREP salvo -> E:\\References\\3D\\alice_para_separar.blend")
print("PREP_DONE")
