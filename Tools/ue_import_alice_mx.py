import unreal
AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")
print("SKEL", skel is not None)

t = unreal.AssetImportTask()
t.set_editor_property("filename", r"E:\References\3D\Alice-T-Pose.fbx")
t.set_editor_property("destination_path", "/Game/Alice/Characters/AliceReal")
t.set_editor_property("destination_name", "SK_AliceReal")
t.set_editor_property("automated", True)
t.set_editor_property("replace_existing", True)
t.set_editor_property("save", True)
ui = unreal.FbxImportUI()
ui.set_editor_property("import_as_skeletal", True)
ui.set_editor_property("import_mesh", True)
ui.set_editor_property("import_animations", False)
ui.set_editor_property("import_materials", False)
ui.set_editor_property("import_textures", False)
ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
if skel:
    ui.set_editor_property("skeleton", skel)
sk_data = ui.get_editor_property("skeletal_mesh_import_data")
sk_data.set_editor_property("import_morph_targets", False)
sk_data.set_editor_property("convert_scene", True)
t.set_editor_property("options", ui)
AT.import_asset_tasks([t])
EAL.save_directory("/Game/Alice/Characters/AliceReal", False, True)

sk = unreal.load_asset("/Game/Alice/Characters/AliceReal/SK_AliceReal")
print("SK_AliceReal", sk is not None)
if sk:
    try:
        b = sk.get_bounds().box_extent
        print("BOUNDS_EXTENT", round(b.x,1), round(b.y,1), round(b.z,1), "height~", round(b.z*2,1))
        print("NUM_MATS", sk.get_num_materials())
    except Exception as e:
        print("bounds err", e)
print("IMPORT_ALICE_MX_DONE")
