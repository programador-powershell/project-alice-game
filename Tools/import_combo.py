"""Import combo + guard clips onto SK_EveM_Skeleton (legacy importer)."""
import os
import unreal

AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
SRC = r"E:\model\anims"
skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")

CLIPS = {
    "A_Atk1":  "Standing Melee Attack Horizontal.fbx",
    "A_Atk2":  "Standing Melee Attack Backhand.fbx",
    "A_Atk3":  "Standing Melee Attack Downward.fbx",
    "A_Block": os.path.join("Pro Sword and Shield Pack", "sword and shield block idle.fbx"),
    "A_Parry": os.path.join("Pro Sword and Shield Pack", "sword and shield block.fbx"),
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
for p in EAL.list_assets("/Game/Alice/AnimM", recursive=True, include_folder=False):
    a = unreal.load_asset(p)
    unreal.log("[Alice] CMB %s = %s" % (p, a.get_class().get_name() if a else "None"))
unreal.log("[Alice] COMBO IMPORT DONE")
