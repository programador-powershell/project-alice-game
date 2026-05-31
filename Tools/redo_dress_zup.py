"""Refaz vestido rigado no armature Z-UP do corpo Mixamo."""
import bpy, mathutils as mu
P=lambda s:print("DZ "+s)
bpy.ops.wm.read_factory_settings(use_empty=True)

bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\alice_RIGGED_zup.fbx", automatic_bone_orientation=True)
arm=next(o for o in bpy.data.objects if o.type=='ARMATURE')
for o in [o for o in bpy.data.objects if o.type=='MESH']:
    bpy.data.objects.remove(o, do_unlink=True)
bb=[arm.matrix_world @ mu.Vector(c) for c in arm.bound_box]
azmin=min(v.z for v in bb); azmax=max(v.z for v in bb); ah=azmax-azmin
P(f"corpo altura={ah:.3f}")

bpy.ops.import_scene.gltf(filepath=r"E:\References\3D\alice-vestido.glb")
dress=next(o for o in bpy.data.objects if o.type=='MESH')
dress.name="Vestido"
bpy.ops.object.select_all(action='DESELECT')
dress.select_set(True); bpy.context.view_layer.objects.active=dress
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

me=dress.data; me.calc_loop_triangles()
tris0=len(me.loop_triangles)
ratio=min(1.0,120000/max(1,tris0))
d=dress.modifiers.new("D",'DECIMATE'); d.decimate_type='COLLAPSE'; d.ratio=ratio
bpy.ops.object.modifier_apply(modifier="D")
me=dress.data; me.calc_loop_triangles()
P(f"vestido tris {tris0}->{len(me.loop_triangles)}")

bb=[dress.matrix_world @ mu.Vector(c) for c in dress.bound_box]
dh=max(v.z for v in bb)-min(v.z for v in bb)
if dh>0.001:
    sf=ah/dh; dress.scale=(sf,sf,sf)
    bpy.ops.object.select_all(action='DESELECT')
    dress.select_set(True); bpy.context.view_layer.objects.active=dress
    bpy.ops.object.transform_apply(scale=True)
    P(f"sf={sf:.3f}")
bb=[dress.matrix_world @ mu.Vector(c) for c in dress.bound_box]
dcx=(min(v.x for v in bb)+max(v.x for v in bb))/2
dcy=(min(v.y for v in bb)+max(v.y for v in bb))/2
dzmin=min(v.z for v in bb)
dress.location=(-dcx,-dcy,-dzmin)
bpy.context.view_layer.update()

bpy.ops.object.select_all(action='DESELECT')
dress.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active=arm
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
P(f"vgroups={len(dress.vertex_groups)}")

for o in bpy.data.objects: o.select_set(o.type in ('MESH','ARMATURE'))
bpy.ops.export_scene.fbx(
    filepath=r"E:\References\3D\alice_vestido_zup.fbx",
    use_selection=True, object_types={'MESH','ARMATURE'},
    add_leaf_bones=False, bake_anim=False, path_mode='COPY', embed_textures=True,
    axis_forward='-Z', axis_up='Y',
    primary_bone_axis='Y', secondary_bone_axis='X',
    apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL',
    mesh_smooth_type='FACE')
P("DZDONE")
