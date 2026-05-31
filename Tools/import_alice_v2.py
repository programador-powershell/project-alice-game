"""Importa SK_Alice_V2.fbx garantindo skin weights multi-influencia.
Reusa o skeleton SK_AliceOficial_Skeleton (mesmos 49 bones -> anims ja servem).
Confirma MaxBoneInfluences>1. Atribui ao BP_Alice.
"""
import unreal, os
L = lambda s: unreal.log(f"[V2] {s}")

FBX = r"E:\model\SK_Alice_V2.fbx"
L(f"FBX {os.path.getsize(FBX)//1024}KB")
DST = "/Game/Alice/Characters/AliceV2"
unreal.EditorAssetLibrary.make_directory(DST)

task = unreal.AssetImportTask()
task.filename = FBX
task.destination_path = DST
task.destination_name = "SK_AliceV2"
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
# reusa skeleton oficial pra anims ja importados servirem
opt.skeleton = unreal.load_asset("/Game/Alice/Characters/AliceOficial/SK_AliceOficial_Skeleton")
sid = opt.skeletal_mesh_import_data
sid.set_editor_property("import_morph_targets", False)
# garante que mantem as influencias do FBX
try:
    sid.set_editor_property("threshold_position", 0.0)
except Exception: pass
task.options = opt

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
L(f"imported: {task.imported_object_paths}")

sk = unreal.load_asset(f"{DST}/SK_AliceV2")
if not sk:
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for a in ar.get_assets_by_path(DST, recursive=True):
        if str(a.asset_class_path.asset_name)=="SkeletalMesh":
            sk = unreal.load_asset(str(a.package_name))

d = unreal.EditorAssetLibrary.find_asset_data(sk.get_path_name())
for tag in ("Vertices","Bones","MaxBoneInfluences"):
    v = d.get_tag_value(tag)
    if v: L(f"  {tag} = {v}")
L(f"  skeleton = {sk.skeleton.get_name() if sk.skeleton else None}")
for i,m in enumerate(sk.materials):
    mi=m.material_interface
    L(f"  mat[{i}] = {mi.get_name() if mi else 'None'}")

# atribui ao BP
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
cdo = unreal.get_default_object(bp.generated_class())
mc = cdo.get_editor_property("mesh")
mc.set_editor_property("skeletal_mesh_asset", sk)
mc.set_editor_property("anim_class", None)
mc.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
mc.set_editor_property("relative_rotation", unreal.Rotator(roll=0,pitch=0,yaw=-90))
mc.set_editor_property("relative_location", unreal.Vector(0,0,-88))
unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
L("BP_Alice.mesh = SK_AliceV2  SAVED")
L("END")
