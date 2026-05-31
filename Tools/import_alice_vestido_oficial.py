"""Importa E:\model\SK_Alice_Vestido.fbx (vestido + rig Alice-T-Pose 49 bones + textura).
Cria skeleton NOVO (SK_AliceOficial_Skeleton). Depois os anims serao importados
nesse skeleton (compativeis por nome). Atribui ao BP_Alice.
"""
import unreal, os
L = lambda s: unreal.log(f"[AV] {s}")

FBX = r"E:\model\SK_Alice_Vestido.fbx"
L(f"FBX exists={os.path.exists(FBX)} size={os.path.getsize(FBX)//1024}KB")
DST = "/Game/Alice/Characters/AliceOficial"
unreal.EditorAssetLibrary.make_directory(DST)

task = unreal.AssetImportTask()
task.filename = FBX
task.destination_path = DST
task.destination_name = "SK_AliceOficial"
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
# skeleton = None -> cria um novo a partir deste FBX (rig oficial da Alice)
task.options = opt

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
L(f"imported: {task.imported_object_paths}")

ar = unreal.AssetRegistryHelpers.get_asset_registry()
sk = None; skel = None
for a in ar.get_assets_by_path(DST, recursive=True):
    cls = str(a.asset_class_path.asset_name)
    L(f"  {cls} {str(a.package_name)}")
    if cls == "SkeletalMesh": sk = unreal.load_asset(str(a.package_name))
    if cls == "Skeleton": skel = unreal.load_asset(str(a.package_name))

if not sk:
    L("ABORT sem mesh"); raise SystemExit
L(f"skeleton = {sk.skeleton.get_name() if sk.skeleton else None}")
bt = sk.skeleton.get_editor_property("bone_tree") if sk.skeleton else []
L(f"bones = {len(bt)}")
for i,m in enumerate(sk.materials):
    mi = m.material_interface
    L(f"  mat[{i}] = {mi.get_name() if mi else 'None'}")

# atribui ao BP_Alice
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")
mc.set_editor_property("skeletal_mesh_asset", sk)
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP_Alice.mesh = SK_AliceOficial  SAVED")
L("DONE — proximo: importar anims nesse skeleton")
