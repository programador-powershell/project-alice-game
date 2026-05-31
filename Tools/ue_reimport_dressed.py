import unreal
AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")
dest = "/Game/Alice/Characters/AliceDressed"; name = "SK_AliceDressed"
t = unreal.AssetImportTask()
t.set_editor_property("filename", r"E:\References\3D\SK_AliceDress.fbx")
t.set_editor_property("destination_path", dest); t.set_editor_property("destination_name", name)
t.set_editor_property("automated", True); t.set_editor_property("replace_existing", True); t.set_editor_property("save", True)
ui = unreal.FbxImportUI()
ui.set_editor_property("import_as_skeletal", True); ui.set_editor_property("import_mesh", True)
ui.set_editor_property("import_animations", False); ui.set_editor_property("import_materials", False); ui.set_editor_property("import_textures", False)
ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
if skel: ui.set_editor_property("skeleton", skel)
t.set_editor_property("options", ui)
AT.import_asset_tasks([t]); EAL.save_directory(dest, False, True)
import unreal as u
ar = u.AssetRegistryHelpers.get_asset_registry()
for a in ar.get_assets_by_path(dest, recursive=True):
    print("ASSET", a.asset_name, "|", a.asset_class_path.asset_name)
sk = unreal.load_asset(dest + "/" + name)
print("class", sk.get_class().get_name() if sk else None)
print("REIMPORT_DRESSED_DONE")
