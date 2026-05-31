"""Importa coelho-vestidoT-Pose e chapeleiro-T-Pose (mixamo-rigados) e le
MaxBoneInfluences. Se for >1 = mixamo da pesos bons (e o auto-weight da Alice que e ruim).
Isso decide a estrategia: usar mixamo online pra Alice tambem."""
import unreal, os
L = lambda s: unreal.log(f"[BW] {s}")

for fbx, name in [
    (r"E:\References\3D\coelho-vestidoT-Pose.fbx", "SK_CoelhoVest"),
    (r"E:\References\3D\chapeleiro-T-Pose.fbx", "SK_ChapeleiroT"),
]:
    DST = f"/Game/Alice/Characters/_wtest"
    unreal.EditorAssetLibrary.make_directory(DST)
    task = unreal.AssetImportTask()
    task.filename = fbx
    task.destination_path = DST
    task.destination_name = name
    task.replace_existing = True
    task.automated = True
    task.save = False
    opt = unreal.FbxImportUI()
    opt.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
    opt.import_mesh = True
    opt.import_as_skeletal = True
    opt.import_animations = False
    opt.import_materials = False
    task.options = opt
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    sk = unreal.load_asset(f"{DST}/{name}")
    if sk:
        d = unreal.EditorAssetLibrary.find_asset_data(sk.get_path_name())
        L(f"{name}: verts={d.get_tag_value('Vertices')} bones={d.get_tag_value('Bones')} MaxInfluences={d.get_tag_value('MaxBoneInfluences')}")
    else:
        L(f"{name}: import falhou")
L("END")
