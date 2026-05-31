"""Importa SK_AliceVestido.fbx (rig completo + textura) no UE no SK_EveM_Skeleton,
COM materiais, e atribui ao BP_Alice. Resolve estatua + cor de uma vez.
"""
import unreal, os
L = lambda s: unreal.log(f"[imp] {s}")

FBX = r"E:\model\SK_AliceVestido.fbx"
L(f"FBX exists={os.path.exists(FBX)} size={os.path.getsize(FBX)//1024}KB")
DST = "/Game/Alice/Characters/AliceVestido"
unreal.EditorAssetLibrary.make_directory(DST)

task = unreal.AssetImportTask()
task.filename = FBX
task.destination_path = DST
task.destination_name = "SK_AliceVestido"
task.replace_existing = True
task.automated = True
task.save = True

opt = unreal.FbxImportUI()
opt.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
opt.import_mesh = True
opt.import_as_skeletal = True
opt.import_materials = True
opt.import_textures = True
opt.import_animations = False
opt.create_physics_asset = True
opt.skeleton = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")
sid = opt.skeletal_mesh_import_data
sid.set_editor_property("import_morph_targets", False)
task.options = opt

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
L(f"imported: {task.imported_object_paths}")

ar = unreal.AssetRegistryHelpers.get_asset_registry()
sk = None
for a in ar.get_assets_by_path(DST, recursive=True):
    cls = str(a.asset_class_path.asset_name)
    L(f"  {cls} {str(a.package_name)}")
    if cls == "SkeletalMesh":
        sk = unreal.load_asset(str(a.package_name))

if not sk:
    L("ABORT sem SkeletalMesh"); raise SystemExit

for i,m in enumerate(sk.materials):
    mi = m.material_interface
    L(f"  mat[{i}] = {mi.get_name() if mi else 'None'}")

bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")
mc.set_editor_property("skeletal_mesh_asset", sk)
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP_Alice.mesh = SK_AliceVestido  SAVED")
L("DONE")
