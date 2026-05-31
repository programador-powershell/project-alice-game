"""
Headless asset import for Alice. Imports all character/boss/mob GLBs and prop GLBs
into /Game/Alice via the Interchange glTF pipeline, then saves.

Run:
  UnrealEditor-Cmd.exe E:\Alice\Alice.uproject -ExecutePythonScript="E:\Alice\Tools\import_assets.py"
"""
import unreal
import os

PAIRS = [
    (r"E:\temp_glb_import", "/Game/Alice/Characters"),
    (r"E:\temp_glb_props",  "/Game/Alice/Props"),
]

asset_tools = unreal.AssetToolsHelpers.get_asset_tools()


def import_dir(src_dir, dest_path):
    tasks = []
    for fname in sorted(os.listdir(src_dir)):
        if not fname.lower().endswith(".glb"):
            continue
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", os.path.join(src_dir, fname))
        task.set_editor_property("destination_path", dest_path)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        tasks.append(task)
    if tasks:
        asset_tools.import_asset_tasks(tasks)
    return len(tasks)


def main():
    total = 0
    for src, dest in PAIRS:
        if not os.path.isdir(src):
            unreal.log_warning("[Alice] Missing source dir: %s" % src)
            continue
        n = import_dir(src, dest)
        unreal.log("[Alice] Imported %d GLB from %s -> %s" % (n, src, dest))
        total += n
    unreal.log("[Alice] TOTAL import tasks submitted: %d" % total)
    try:
        unreal.EditorAssetLibrary.save_directory("/Game/Alice", False, True)
    except Exception as e:
        unreal.log_warning("[Alice] save_directory failed: %s" % e)
    unreal.log("[Alice] IMPORT DONE")


main()
