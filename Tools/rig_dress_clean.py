"""Rigga o VESTIDO SEPARADO (sem corpo) no skel do alice_RIGGED_zup (corpo Mixamo Z-up).
Exporta SK_AliceDress final, alinhado, pronto p/ UE."""
import bpy, mathutils as mu
P=lambda s:print("DC "+s)
bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. corpo Z-up (armature)
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\alice_RIGGED_zup.fbx", automatic_bone_orientation=True)
arm=next(o for o in bpy.data.objects if o.type=='ARMATURE')
for o in [o for o in bpy.data.objects if o.type=='MESH']:
    bpy.data.objects.remove(o, do_unlink=True)
bb=[arm.matrix_world @ mu.Vector(c) for c in arm.bound_box]
ah=max(v.z for v in bb)-min(v.z for v in bb)
P(f"armature corpo bones={len(arm.data.bones)} altura={ah:.3f}")

# 2. vestido SEPARADO (sem corpo)
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\alice_vestido_separado.fbx", automatic_bone_orientation=True)
dress=next((o for o in bpy.data.objects if o.type=='MESH'), None)
if not dress: P("ERRO sem vestido"); raise SystemExit
dress.name="Vestido"
bpy.ops.object.select_all(action='DESELECT')
dress.select_set(True); bpy.context.view_layer.objects.active=dress
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
P(f"vestido verts={len(dress.data.vertices)} mats={len(dress.data.materials)}")

# 3. escala vestido pra bater altura corpo
bb=[dress.matrix_world @ mu.Vector(c) for c in dress.bound_box]
dh=max(v.z for v in bb)-min(v.z for v in bb)
if dh>0.001:
    sf=ah/dh; dress.scale=(sf,sf,sf)
    bpy.ops.object.select_all(action='DESELECT')
    dress.select_set(True); bpy.context.view_layer.objects.active=dress
    bpy.ops.object.transform_apply(scale=True)
    P(f"vestido sf={sf:.3f}")

# 4. centra vestido no armature
bb=[dress.matrix_world @ mu.Vector(c) for c in dress.bound_box]
dcx=(min(v.x for v in bb)+max(v.x for v in bb))/2
dcy=(min(v.y for v in bb)+max(v.y for v in bb))/2
dzmin=min(v.z for v in bb)
dress.location=(-dcx,-dcy,-dzmin)
bpy.context.view_layer.update()

# 5. auto-weight no armature corpo
bpy.ops.object.select_all(action='DESELECT')
dress.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active=arm
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
P(f"vgroups={len(dress.vertex_groups)}")

# 6. export Z-up
for o in bpy.data.objects: o.select_set(o.type in ('MESH','ARMATURE'))
bpy.ops.export_scene.fbx(
    filepath=r"E:\References\3D\alice_vestido_FINAL.fbx",
    use_selection=True, object_types={'MESH','ARMATURE'},
    add_leaf_bones=False, bake_anim=False, path_mode='COPY', embed_textures=True,
    axis_forward='-Z', axis_up='Y',
    primary_bone_axis='Y', secondary_bone_axis='X',
    apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL',
    mesh_smooth_type='FACE')
P("export -> alice_vestido_FINAL.fbx")
P("DCDONE")
