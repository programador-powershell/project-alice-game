"""
Consistent-skeleton import: skeletal mesh + all clips from the SAME Blender armature.
Eve_Skel.fbx -> SK_EveB (+ SK_EveB_Skeleton); armature-only clips -> AnimSequences on it.
Interchange-FBX is disabled via DefaultEngine.ini [ConsoleVariables] -> legacy importer.
"""
import os
import unreal

AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary

for d in ("/Game/Alice/Animations", "/Game/Alice/Characters/EveB"):
    try:
        if EAL.does_directory_exist(d):
            EAL.delete_directory(d)
    except Exception as e:
        unreal.log_warning("clean %s: %s" % (d, e))


def imp(fp, dest, name, anim, skel=None):
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", fp)
    t.set_editor_property("destination_path", dest)
    t.set_editor_property("destination_name", name)
    t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("save", True)
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_as_skeletal", True)
    if anim:
        ui.set_editor_property("import_mesh", False)
        ui.set_editor_property("import_animations", True)
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
        if skel:
            ui.set_editor_property("skeleton", skel)
    else:
        ui.set_editor_property("import_mesh", True)
        ui.set_editor_property("import_animations", False)
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    t.set_editor_property("options", ui)
    return t


# 1) Skeletal mesh
AT.import_asset_tasks([imp(r"E:\model\anims\Eve_Skel.fbx", "/Game/Alice/Characters/EveB", "SK_EveB", False)])
EAL.save_directory("/Game/Alice/Characters/EveB", False, True)
skel = unreal.load_asset("/Game/Alice/Characters/EveB/SK_EveB_Skeleton")
unreal.log("[Alice] EveB skeleton loaded: %s" % (skel is not None))

# 2) Animations onto that skeleton
CLIPS = ["Eve_Idle", "Eve_Walk", "Eve_Run", "Eve_Attack", "Eve_Dodge", "Eve_Hit", "Eve_Death"]
tasks = []
for c in CLIPS:
    fp = r"E:\model\anims\%s.fbx" % c
    if os.path.exists(fp):
        tasks.append(imp(fp, "/Game/Alice/Animations", "A_%s" % c, True, skel))
AT.import_asset_tasks(tasks)
EAL.save_directory("/Game/Alice/Animations", False, True)

for p in EAL.list_assets("/Game/Alice/Animations", recursive=True, include_folder=False):
    a = unreal.load_asset(p)
    unreal.log("[Alice] FULL %s class=%s" % (p, a.get_class().get_name() if a else "None"))
unreal.log("[Alice] FULL DONE")
