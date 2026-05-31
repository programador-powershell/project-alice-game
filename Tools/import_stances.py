"""Import per-dress weapon stance clips onto SK_EveM_Skeleton."""
import os
import unreal

AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
SRC = r"E:\model\anims"
skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")

CLIPS = {
    "A_GS_Idle":  os.path.join("Great Sword Pack", "great sword idle.fbx"),
    "A_GS_Atk":   os.path.join("Great Sword Pack", "great sword slash.fbx"),
    "A_GS_Run":   os.path.join("Great Sword Pack", "great sword run.fbx"),
    "A_Dual_Atk": "Dual Weapon Combo.fbx",
    "A_SS_Idle":  os.path.join("Pro Sword and Shield Pack", "sword and shield idle.fbx"),
    "A_SS_Atk":   os.path.join("Pro Sword and Shield Pack", "sword and shield slash.fbx"),
}


def task(fp, name):
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", fp)
    t.set_editor_property("destination_path", "/Game/Alice/AnimM")
    t.set_editor_property("destination_name", name)
    t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("save", True)
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_as_skeletal", True)
    ui.set_editor_property("import_mesh", False)
    ui.set_editor_property("import_animations", True)
    ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
    if skel:
        ui.set_editor_property("skeleton", skel)
    t.set_editor_property("options", ui)
    return t


tasks = []
for name, rel in CLIPS.items():
    fp = os.path.join(SRC, rel)
    if os.path.exists(fp):
        tasks.append(task(fp, name))
    else:
        unreal.log_warning("[Alice] missing %s" % fp)
if tasks:
    AT.import_asset_tasks(tasks)
    EAL.save_directory("/Game/Alice/AnimM", False, True)
unreal.log("[Alice] STANCES IMPORT DONE")
