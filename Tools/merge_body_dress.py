"""DO ZERO: junta corpo (Mixamo riggado Z-up) + vestido separado num UNICO mesh skeletal.
- corpo alice_RIGGED_zup.fbx (armature 33 bones + pesos)
- vestido alice_vestido_separado.fbx (so mesh)
- vestido ganha pesos (auto-weight no mesmo armature)
- junta os 2 meshes (Ctrl+J) = 1 skeletal
- export alice_FULL_rigged.fbx
"""
import bpy, mathutils as mu
P=lambda s:print("MG "+s)
bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. CORPO zup (armature + mesh + pesos Mixamo)
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\alice_RIGGED_zup.fbx", automatic_bone_orientation=True)
arm=next(o for o in bpy.data.objects if o.type=='ARMATURE')
corpo=next(o for o in bpy.data.objects if o.type=='MESH')
corpo.name="Corpo"
P(f"corpo verts={len(corpo.data.vertices)} vgroups={len(corpo.vertex_groups)} armbones={len(arm.data.bones)}")
bb=[corpo.matrix_world @ mu.Vector(c) for c in corpo.bound_box]
ah=max(v.z for v in bb)-min(v.z for v in bb)
acx=(min(v.x for v in bb)+max(v.x for v in bb))/2
acy=(min(v.y for v in bb)+max(v.y for v in bb))/2
azmin=min(v.z for v in bb)
P(f"corpo altura={ah:.3f}")

# 2. VESTIDO separado (so mesh)
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\alice_vestido_separado.fbx", automatic_bone_orientation=True)
vestido=next((o for o in bpy.data.objects if o.type=='MESH' and o.name!="Corpo"), None)
vestido.name="Vestido"
bpy.ops.object.select_all(action='DESELECT')
vestido.select_set(True); bpy.context.view_layer.objects.active=vestido
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
P(f"vestido verts={len(vestido.data.vertices)}")

# 3. alinha vestido ao corpo (escala + centra)
bb=[vestido.matrix_world @ mu.Vector(c) for c in vestido.bound_box]
dh=max(v.z for v in bb)-min(v.z for v in bb)
if dh>0.001:
    sf=ah/dh; vestido.scale=(sf,sf,sf)
    bpy.ops.object.select_all(action='DESELECT')
    vestido.select_set(True); bpy.context.view_layer.objects.active=vestido
    bpy.ops.object.transform_apply(scale=True)
    P(f"vestido sf={sf:.3f}")
bb=[vestido.matrix_world @ mu.Vector(c) for c in vestido.bound_box]
vcx=(min(v.x for v in bb)+max(v.x for v in bb))/2
vcy=(min(v.y for v in bb)+max(v.y for v in bb))/2
vzmin=min(v.z for v in bb)
vestido.location=(acx-vcx, acy-vcy, azmin-vzmin)
bpy.context.view_layer.update()
P("vestido alinhado ao corpo")

# 4. auto-weight vestido no MESMO armature
bpy.ops.object.select_all(action='DESELECT')
vestido.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active=arm
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
P(f"vestido vgroups={len(vestido.vertex_groups)}")

# 5. JUNTA corpo+vestido em 1 mesh (ambos ja parenteados ao armature)
bpy.ops.object.select_all(action='DESELECT')
vestido.select_set(True); corpo.select_set(True)
bpy.context.view_layer.objects.active=corpo  # corpo = ativo, resultado herda nome/pesos
bpy.ops.object.join()
merged=bpy.context.view_layer.objects.active
P(f"MERGED verts={len(merged.data.vertices)} vgroups={len(merged.vertex_groups)} mats={len(merged.data.materials)}")

# 6. export
bpy.ops.object.select_all(action='DESELECT')
merged.select_set(True); arm.select_set(True)
bpy.context.view_layer.objects.active=arm
bpy.ops.export_scene.fbx(
    filepath=r"E:\References\3D\alice_FULL_rigged.fbx",
    use_selection=True, object_types={'MESH','ARMATURE'},
    add_leaf_bones=False, bake_anim=False, path_mode='COPY', embed_textures=True,
    axis_forward='-Z', axis_up='Y',
    primary_bone_axis='Y', secondary_bone_axis='X',
    apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL',
    mesh_smooth_type='FACE')
P("export -> alice_FULL_rigged.fbx")
P("MGDONE")
