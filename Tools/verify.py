"""
Headless verification: load L_Arena, report what's actually in it, attempt a screenshot.
  UnrealEditor-Cmd.exe E:\Alice\Alice.uproject -ExecutePythonScript=E:\Alice\Tools\verify.py
"""
import unreal

LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

ok = LES.load_level("/Game/Alice/Maps/L_Arena")
unreal.log("[Alice][VERIFY] load L_Arena -> %s" % ok)

actors = EAS.get_all_level_actors()
counts = {}
boss = None
checkpoint = None
player_start = None
for a in actors:
    n = type(a).__name__
    counts[n] = counts.get(n, 0) + 1
    if "Coelho" in n or "Boss" in n:
        boss = a
    if "Checkpoint" in n:
        checkpoint = a
    if "PlayerStart" in n:
        player_start = a

unreal.log("[Alice][VERIFY] total actors: %d" % len(actors))
for k in sorted(counts):
    unreal.log("[Alice][VERIFY]   %-28s %d" % (k, counts[k]))

unreal.log("[Alice][VERIFY] boss present:        %s" % (boss is not None))
unreal.log("[Alice][VERIFY] checkpoint present:  %s" % (checkpoint is not None))
unreal.log("[Alice][VERIFY] player start present:%s" % (player_start is not None))

# Confirm key imported assets exist
EAL = unreal.EditorAssetLibrary
for p in ["/Game/Alice/Characters/SM_Alice_3D",
          "/Game/Alice/Characters/SM_coelho_boss",
          "/Game/Alice/Blueprints/BP_Alice",
          "/Game/Alice/Blueprints/BP_AliceGameMode"]:
    unreal.log("[Alice][VERIFY] asset %s -> %s" % (p, EAL.does_asset_exist(p)))

try:
    unreal.AutomationLibrary.take_high_res_screenshot(1600, 900, "alice_arena.png")
    unreal.log("[Alice][VERIFY] screenshot requested (Saved/Screenshots)")
except Exception as e:
    unreal.log_warning("[Alice][VERIFY] screenshot failed: %s" % e)

unreal.log("[Alice][VERIFY] DONE")
