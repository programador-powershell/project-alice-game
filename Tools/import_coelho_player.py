"""Importa coelho-vestidoT-Pose (mixamo-rigado, pesos bons) como SkeletalMesh
com skeleton proprio + material. Sera o player temporario pra testar movimento.
"""
import unreal, os
L = lambda s: unreal.log(f"[CP] {s}")

FBX = r"E:\References\3D\coelho-vestidoT-Pose.fbx"
L(f"FBX {os.path.getsize(FBX)//1024}KB")
DST = "/Game/Alice/Characters/CoelhoPlayer"
unreal.EditorAssetLibrary.make_directory(DST)

task = unreal.AssetImportTask()
task.filename = FBX
task.destination_path = DST
task.destination_name = "SK_CoelhoPlayer"
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
# skeleton None = cria proprio (41 bones do coelho)
task.options = opt

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
L(f"imported: {task.imported_object_paths}")

ar = unreal.AssetRegistryHelpers.get_asset_registry()
sk=None; skel=None
for a in ar.get_assets_by_path(DST, recursive=True):
    cls=str(a.asset_class_path.asset_name)
    L(f"  {cls} {str(a.package_name)}")
    if cls=="SkeletalMesh": sk=unreal.load_asset(str(a.package_name))
    if cls=="Skeleton": skel=unreal.load_asset(str(a.package_name))

if not sk: L("ABORT"); raise SystemExit
d = unreal.EditorAssetLibrary.find_asset_data(sk.get_path_name())
L(f"verts={d.get_tag_value('Vertices')} bones={d.get_tag_value('Bones')} maxInfl={d.get_tag_value('MaxBoneInfluences')}")
L(f"skeleton={sk.skeleton.get_name() if sk.skeleton else None}")
for i,m in enumerate(sk.materials):
    mi=m.material_interface
    L(f"  mat[{i}]={mi.get_name() if mi else None}")
L("DONE")
