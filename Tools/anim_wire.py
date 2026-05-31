"""
ONE-SHOT — run after dropping Mixamo animation FBXs into E:\model\anims.
Imports them as AnimSequences onto SK_EveB_Skeleton (legacy importer; Interchange-FBX is
disabled in DefaultEngine.ini), sets SK_EveB as the player mesh, and wires clips to the
BP_Alice Anim_* slots by filename keyword (idle/walk/run/attack/dodge/hit/death).

  UnrealEditor-Cmd.exe E:\Alice\Alice.uproject -ExecutePythonScript=E:\Alice\Tools\anim_wire.py
"""
import os
import unreal

EAL = unreal.EditorAssetLibrary
AT = unreal.AssetToolsHelpers.get_asset_tools()
ANIM_DIR = "/Game/Alice/Animations"
SRC = r"E:\model\anims"

skel = unreal.load_asset("/Game/Alice/Characters/EveB/SK_EveB_Skeleton")
sk = unreal.load_asset("/Game/Alice/Characters/EveB/SK_EveB")

# Import every FBX in the drop folder as an animation on the Eve skeleton.
tasks = []
for f in sorted(os.listdir(SRC)) if os.path.isdir(SRC) else []:
    if not f.lower().endswith(".fbx"):
        continue
    name = "A_" + os.path.splitext(f)[0].replace(" ", "_")
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", os.path.join(SRC, f))
    t.set_editor_property("destination_path", ANIM_DIR)
    t.set_editor_property("destination_name", name)
    t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("save", True)
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_mesh", False)
    ui.set_editor_property("import_as_skeletal", True)
    ui.set_editor_property("import_animations", True)
    ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
    if skel:
        ui.set_editor_property("skeleton", skel)
    t.set_editor_property("options", ui)
    tasks.append(t)
if tasks:
    AT.import_asset_tasks(tasks)
    EAL.save_directory(ANIM_DIR, False, True)

# Wire by keyword.
slotmap = {
    "idle": "anim_idle", "walk": "anim_walk", "run": "anim_run", "jog": "anim_run",
    "attack": "anim_attack", "slash": "anim_attack", "combo": "anim_attack",
    "dodge": "anim_dodge", "roll": "anim_dodge", "evade": "anim_dodge",
    "hit": "anim_hit", "impact": "anim_hit", "react": "anim_hit",
    "death": "anim_death", "die": "anim_death", "dying": "anim_death",
}
bp = unreal.load_asset("/Game/Alice/Blueprints/BP_Alice")
if bp:
    cdo = unreal.get_default_object(bp.generated_class())
    if sk:
        try:
            cdo.get_editor_property("mesh").set_skeletal_mesh_asset(sk)
            cdo.set_editor_property("visual_mesh_asset", None)
        except Exception as e:
            print("ANIMWIRE mesh:", e)
    for p in EAL.list_assets(ANIM_DIR, recursive=True, include_folder=False):
        a = unreal.load_asset(p)
        if not isinstance(a, unreal.AnimSequence):
            continue
        low = p.lower()
        for kw, slot in slotmap.items():
            if kw in low:
                try:
                    cdo.set_editor_property(slot, a)
                    print("ANIMWIRE", slot, "<-", p)
                except Exception as e:
                    print("ANIMWIRE set", slot, e)
                break
    try:
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        EAL.save_asset("/Game/Alice/Blueprints/BP_Alice")
    except Exception as e:
        print("ANIMWIRE compile:", e)
print("ANIMWIRE DONE")
