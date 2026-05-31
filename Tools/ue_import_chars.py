import unreal
AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")
print("SKEL", skel is not None)

def imp(fbx, dest, name):
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", fbx)
    t.set_editor_property("destination_path", dest)
    t.set_editor_property("destination_name", name)
    t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("save", True)
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_as_skeletal", True)
    ui.set_editor_property("import_mesh", True)
    ui.set_editor_property("import_materials", False)
    ui.set_editor_property("import_textures", False)
    ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    if skel:
        ui.set_editor_property("skeleton", skel)
    t.set_editor_property("options", ui)
    AT.import_asset_tasks([t])
    EAL.save_directory(dest, False, True)
    a = unreal.load_asset(dest + "/" + name)
    print("IMPORTED", name, a is not None)
    return a

imp(r"E:\References\3D\SK_Alice.fbx", "/Game/Alice/Characters/AliceReal", "SK_AliceReal")
imp(r"E:\References\3D\SK_Lidia.fbx", "/Game/Alice/Characters/LidiaReal", "SK_LidiaReal")
print("IMPORT_CHARS_DONE")
