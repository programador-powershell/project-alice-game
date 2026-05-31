"""Reimporta Alice-T-Pose.fbx (Mixamo, skin perfeito) como SK_AliceReal
e troca o mesh do BP_Alice pra ela. Soluciona 'estátua deslizante'.
"""
import unreal, os
L = lambda s: unreal.log(f"[reimport] {s}")

FBX = r"E:\References\3D\Alice-T-Pose.fbx"
DST_FOLDER = "/Game/Alice/Characters/AliceReal"
SK_NAME = "SK_AliceReal"
BP_PATH = "/Game/Alice/Blueprints/BP_Alice"

L(f"FBX exists = {os.path.exists(FBX)}")
if not os.path.exists(FBX):
    L("ABORT — FBX nao existe"); raise SystemExit

# Garante a pasta
unreal.EditorAssetLibrary.make_directory(DST_FOLDER)

# Task de import
task = unreal.AssetImportTask()
task.filename = FBX
task.destination_path = DST_FOLDER
task.destination_name = SK_NAME
task.replace_existing = True
task.automated = True
task.save = True

opt = unreal.FbxImportUI()
opt.import_mesh = True
opt.import_as_skeletal = True
opt.import_materials = False
opt.import_textures = False
opt.import_animations = False
opt.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
opt.skeletal_mesh_import_data.set_editor_property("import_morph_targets", False)
opt.skeletal_mesh_import_data.set_editor_property("update_skeleton_reference_pose", False)
opt.skeletal_mesh_import_data.set_editor_property("use_t0_as_ref_pose", True)
# usa o esqueleto SK_EveM_Skeleton existente pra anims compatibilizarem
existing_skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")
if existing_skel:
    opt.skeleton = existing_skel
    L(f"reusing skeleton SK_EveM_Skeleton (anims compativeis)")
else:
    L("⚠ SK_EveM_Skeleton ausente — vai criar skeleton novo (anims podem nao funcionar)")
task.options = opt

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
L(f"import task done. imported: {task.imported_object_paths}")

# Confirma asset existe
sk_real = unreal.load_asset(f"{DST_FOLDER}/{SK_NAME}")
L(f"SK_AliceReal load = {'OK' if sk_real else 'MISS'}")

if sk_real:
    bp = unreal.load_asset(BP_PATH)
    cdo = unreal.get_default_object(bp.generated_class())
    mc = cdo.get_editor_property("mesh")
    mc.set_editor_property("skeletal_mesh_asset", sk_real)
    # Mantem rotacao em pe (a sessao anterior ja fixou pitch=0 yaw=-90)
    mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
    unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
    L(f"BP_Alice.mesh.skeletal = SK_AliceReal + rot pitch=0 yaw=-90  SAVED")

L("DONE — da Play e Alice DEVE animar agora (nua, mas com Walk/Run/Atk reais)")
