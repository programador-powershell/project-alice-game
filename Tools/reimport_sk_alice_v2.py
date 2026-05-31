"""Limpa AliceReal velho (anim falsa + phys orfa) e re-importa SK_AliceDress.fbx (10MB, tem mesh)
como SK_AliceDressed_v2 reutilizando SK_EveM_Skeleton.
Se vier mesh real desta vez, troca BP_Alice pra ela."""
import unreal, os

L = lambda s: unreal.log(f"[ri2] {s}")

# limpa AliceReal velho
for p in ("/Game/Alice/Characters/AliceReal/SK_AliceReal",
          "/Game/Alice/Characters/AliceReal/SK_AliceReal_PhysicsAsset"):
    if unreal.EditorAssetLibrary.does_asset_exist(p):
        unreal.EditorAssetLibrary.delete_asset(p)
        L(f"deletado: {p}")

FBX = r"E:\References\3D\SK_AliceDress.fbx"
L(f"FBX exists = {os.path.exists(FBX)}  size = {os.path.getsize(FBX)//1024} KB")

DST = "/Game/Alice/Characters/AliceDressed_v2"
unreal.EditorAssetLibrary.make_directory(DST)

task = unreal.AssetImportTask()
task.filename = FBX
task.destination_path = DST
task.destination_name = "SK_AliceDressed_v2"
task.replace_existing = True
task.automated = True
task.save = True

opt = unreal.FbxImportUI()
opt.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
opt.import_mesh = True
opt.import_as_skeletal = True
opt.import_materials = False
opt.import_textures = False
opt.import_animations = False
opt.create_physics_asset = True
# tenta reusar skeleton — se falhar (incompatibilidade), depois tento sem
opt.skeleton = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")
task.options = opt

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
L(f"imported: {task.imported_object_paths}")

# inspeciona o que veio
ar = unreal.AssetRegistryHelpers.get_asset_registry()
sk = None
for a in ar.get_assets_by_path(DST, recursive=True):
    cls = str(a.asset_class_path.asset_name)
    L(f"  {cls:20s}  {str(a.package_name)}")
    if cls == "SkeletalMesh":
        sk = unreal.load_asset(str(a.package_name))

if sk:
    L(f"SK MESH OK = {sk.get_path_name()}")
    L(f"  skeleton = {sk.skeleton.get_path_name() if sk.skeleton else None}")
    # troca BP_Alice
    bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
    cdo = unreal.get_default_object(bp.generated_class())
    mc = cdo.get_editor_property("mesh")
    mc.set_editor_property("skeletal_mesh_asset", sk)
    mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
    mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
    unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
    L(f"BP_Alice.mesh = SK_AliceDressed_v2  SAVED")
else:
    L("⚠ Nao veio SkeletalMesh do import — FBX talvez sem mesh ou skel incompatível")

L("END")
