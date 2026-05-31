"""Import the authored clip FBXs as AnimSequences onto SK_Eve_Skeleton (legacy FBX importer)."""
import os
import unreal

# Route FBX through the legacy importer so FbxImportUI (incl. target skeleton) is honored.
try:
    unreal.SystemLibrary.execute_console_command(None, "Interchange.FeatureFlags.Import.FBX 0")
    unreal.log("[Alice] Interchange FBX disabled (legacy importer)")
except Exception as e:
    unreal.log_warning("cvar: %s" % e)

skel = unreal.load_asset("/Game/Alice/Characters/Eve/SK_Eve_Skeleton")
unreal.log("[Alice] skeleton loaded: %s" % (skel is not None))

# Clean junk from the prior (wrong) import.
try:
    if unreal.EditorAssetLibrary.does_directory_exist("/Game/Alice/Animations"):
        unreal.EditorAssetLibrary.delete_directory("/Game/Alice/Animations")
        unreal.log("[Alice] cleaned /Game/Alice/Animations")
except Exception as e:
    unreal.log_warning("clean: %s" % e)
AT = unreal.AssetToolsHelpers.get_asset_tools()
CLIPS = ["Eve_Idle", "Eve_Walk", "Eve_Run", "Eve_Attack", "Eve_Dodge", "Eve_Hit", "Eve_Death"]

tasks = []
for c in CLIPS:
    fp = r"E:\model\anims\%s.fbx" % c
    if not os.path.exists(fp):
        unreal.log_warning("[Alice] missing %s" % fp)
        continue
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", fp)
    t.set_editor_property("destination_path", "/Game/Alice/Animations")
    t.set_editor_property("destination_name", "A_%s" % c)
    t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("save", True)
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_mesh", False)
    ui.set_editor_property("import_as_skeletal", True)
    ui.set_editor_property("import_animations", True)
    ui.set_editor_property("skeleton", skel)
    ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
    t.set_editor_property("options", ui)
    tasks.append(t)

AT.import_asset_tasks(tasks)
try:
    unreal.EditorAssetLibrary.save_directory("/Game/Alice/Animations", False, True)
except Exception as e:
    unreal.log_warning("save: %s" % e)
for p in unreal.EditorAssetLibrary.list_assets("/Game/Alice/Animations", recursive=True, include_folder=False):
    unreal.log("[Alice] ANIM_ASSET %s" % p)
unreal.log("[Alice] ANIM_IMPORT DONE")
