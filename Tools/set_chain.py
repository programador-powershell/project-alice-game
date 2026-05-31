"""Wire the 6 boss arenas into a progression: beating a boss loads the next map."""
import unreal

LES = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
EAS = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

CHAIN = [
    ("/Game/Alice/Maps/L_Arena", "L_FlorestaCheshire"),
    ("/Game/Alice/Maps/L_FlorestaCheshire", "L_SalaoCha"),
    ("/Game/Alice/Maps/L_SalaoCha", "L_NevoaCogumelos"),
    ("/Game/Alice/Maps/L_NevoaCogumelos", "L_PatioReal"),
    ("/Game/Alice/Maps/L_PatioReal", "L_CampoEtereo"),
    ("/Game/Alice/Maps/L_CampoEtereo", "L_Arena"),  # loop (NG+)
]

for mappath, nxt in CHAIN:
    if not unreal.EditorAssetLibrary.does_asset_exist(mappath):
        unreal.log_warning("[Alice] missing map %s" % mappath)
        continue
    LES.load_level(mappath)
    n = 0
    for a in EAS.get_all_level_actors():
        if isinstance(a, unreal.BossCharacter):
            a.set_editor_property("next_level_name", unreal.Name(nxt))
            n += 1
    LES.save_current_level()
    unreal.log("[Alice] chained %s -> %s (%d boss)" % (mappath, nxt, n))

unreal.log("[Alice] CHAIN DONE")
