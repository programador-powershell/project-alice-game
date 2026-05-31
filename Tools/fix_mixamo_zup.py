"""Mixamo FBX vem Y-up; UE precisa Z-up. Aplica rotacao+escala no
armature+mesh e re-exporta como alice_RIGGED_zup.fbx."""
import bpy, math
P = lambda s: print("ZU " + s)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=r"E:\References\3D\alice_RIGGED.fbx", automatic_bone_orientation=True)
meshes=[o for o in bpy.data.objects if o.type=='MESH']
arms=[o for o in bpy.data.objects if o.type=='ARMATURE']
P(f"in: meshes={len(meshes)} arms={len(arms)}")

# 1. Aplica transform em TUDO (rotation+scale colapsam no mesh/armature)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
P("transforms aplicados")

# 2. Confirma posicoes pos-apply
for a in arms:
    h=a.data.bones.get("mixamorig:Hips")
    if h: P(f"hips pos-apply head=({h.head_local.x:.2f},{h.head_local.y:.2f},{h.head_local.z:.2f})")

# 3. export Z-up nativo Blender (axis_forward='-Y', axis_up='Z')
for o in bpy.data.objects: o.select_set(o.type in ('MESH','ARMATURE'))
bpy.ops.export_scene.fbx(
    filepath=r"E:\References\3D\alice_RIGGED_zup.fbx",
    use_selection=True, object_types={'MESH','ARMATURE'},
    add_leaf_bones=False, bake_anim=False, path_mode='COPY', embed_textures=True,
    axis_forward='-Z', axis_up='Y',  # FBX padrao (UE converte certo)
    mesh_smooth_type='FACE',
    primary_bone_axis='Y', secondary_bone_axis='X',  # Mixamo defaults
    apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL',
    use_armature_deform_only=False)
P("export -> alice_RIGGED_zup.fbx")
P("ZUDONE")
