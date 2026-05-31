"""
Wire the player to real Mixamo animation.
- Import the Mixamo Eve (skinned) as SK_EveM -> exact skeleton the clips were made for.
- Import 7 curated clips as AnimSequences on SK_EveM_Skeleton.
- Set BP_Alice mesh = SK_EveM and assign the Anim_* slots.
Interchange-FBX is disabled in DefaultEngine.ini -> legacy importer (honors options).
"""
import os
import unreal

AT = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
SRC = r"E:\model\anims"

MESH_FBX = os.path.join(SRC, "Pro Sword and Shield Pack", "Eve By J.Gonzales.fbx")

# slot -> relative clip path (curated for an agile one-handed knife fighter)
CLIPS = {
    "anim_idle":   "Standing Idle.fbx",
    "anim_walk":   "Walking.fbx",
    "anim_run":    "Fast Run.fbx",
    "anim_attack": "One Hand Sword Combo.fbx",
    "anim_dodge":  "Sprinting Forward Roll.fbx",
    "anim_hit":    os.path.join("Pro Longbow Pack", "standing react small from front.fbx"),
    "anim_death":  "Standing React Death Forward.fbx",
}


def task(fp, dest, name, is_anim, skel=None):
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", fp)
    t.set_editor_property("destination_path", dest)
    t.set_editor_property("destination_name", name)
    t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("save", True)
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_as_skeletal", True)
    if is_anim:
        ui.set_editor_property("import_mesh", False)
        ui.set_editor_property("import_animations", True)
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
        if skel:
            ui.set_editor_property("skeleton", skel)
    else:
        ui.set_editor_property("import_mesh", True)
        ui.set_editor_property("import_materials", True)
        ui.set_editor_property("import_textures", True)
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    t.set_editor_property("options", ui)
    return t


def main():
    # clean a fresh target
    for d in ("/Game/Alice/Characters/EveM", "/Game/Alice/AnimM"):
        if EAL.does_directory_exist(d):
            EAL.delete_directory(d)

    # 1) skeletal mesh
    if not os.path.exists(MESH_FBX):
        unreal.log_warning("[Alice] MESH_FBX missing: %s" % MESH_FBX)
        return
    AT.import_asset_tasks([task(MESH_FBX, "/Game/Alice/Characters/EveM", "SK_EveM", False)])
    EAL.save_directory("/Game/Alice/Characters/EveM", False, True)
    skel = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM_Skeleton")
    sk = unreal.load_asset("/Game/Alice/Characters/EveM/SK_EveM")
    unreal.log("[Alice] SK_EveM=%s skel=%s" % (sk is not None, skel is not None))

    # 2) clips
    tasks = []
    slot_to_asset = {}
    for slot, rel in CLIPS.items():
        fp = os.path.join(SRC, rel)
        if not os.path.exists(fp):
            unreal.log_warning("[Alice] clip missing: %s" % fp)
            continue
        name = "A_" + slot.replace("anim_", "").capitalize()
        slot_to_asset[slot] = "/Game/Alice/AnimM/%s" % name
        tasks.append(task(fp, "/Game/Alice/AnimM", name, True, skel))
    if tasks:
        AT.import_asset_tasks(tasks)
        EAL.save_directory("/Game/Alice/AnimM", False, True)

    # report classes
    for p in EAL.list_assets("/Game/Alice/AnimM", recursive=True, include_folder=False):
        a = unreal.load_asset(p)
        unreal.log("[Alice] ANM %s = %s" % (p, a.get_class().get_name() if a else "None"))

    # 3) wire BP_Alice
    bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
    if bp and sk:
        cdo = unreal.get_default_object(bp.generated_class())
        try:
            cdo.get_editor_property("mesh").set_skeletal_mesh_asset(sk)
            cdo.set_editor_property("visual_mesh_asset", None)
        except Exception as e:
            unreal.log_warning("[Alice] mesh set: %s" % e)
        for slot, path in slot_to_asset.items():
            a = unreal.load_asset(path)
            if isinstance(a, unreal.AnimSequence):
                try:
                    cdo.set_editor_property(slot, a)
                    unreal.log("[Alice] wired %s" % slot)
                except Exception as e:
                    unreal.log_warning("[Alice] wire %s: %s" % (slot, e))
            else:
                unreal.log_warning("[Alice] %s not AnimSequence (%s)" % (slot, a.get_class().get_name() if a else "None"))
        try:
            unreal.BlueprintEditorLibrary.compile_blueprint(bp)
            EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
        except Exception as e:
            unreal.log_warning("[Alice] bp save: %s" % e)
    unreal.log("[Alice] CURATED ANIM DONE")


main()
