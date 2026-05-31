"""Import Eve.fbx as a skeletal mesh (+ Mixamo skeleton + materials) for the player."""
import unreal

task = unreal.AssetImportTask()
task.set_editor_property("filename", r"E:\model\Eve.fbx")
task.set_editor_property("destination_path", "/Game/Alice/Characters/Eve")
task.set_editor_property("destination_name", "SK_Eve")
task.set_editor_property("automated", True)
task.set_editor_property("replace_existing", True)
task.set_editor_property("save", True)

ui = unreal.FbxImportUI()
ui.set_editor_property("import_mesh", True)
ui.set_editor_property("import_as_skeletal", True)
ui.set_editor_property("import_animations", False)
ui.set_editor_property("import_materials", True)
ui.set_editor_property("import_textures", True)
task.set_editor_property("options", ui)

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
try:
    unreal.EditorAssetLibrary.save_directory("/Game/Alice/Characters/Eve", False, True)
except Exception as e:
    unreal.log_warning("save: %s" % e)

for p in unreal.EditorAssetLibrary.list_assets("/Game/Alice/Characters/Eve", recursive=True, include_folder=False):
    unreal.log("[Alice] EVE_ASSET %s" % p)
unreal.log("[Alice] EVE_IMPORT DONE")
