"""Verifica o GameMode efetivo do L_Arena, o DefaultPawnClass, e se ha PlayerStart.
1a pessoa + estatua = provavelmente pawn errado ou nao possuido."""
import unreal
L = lambda s: unreal.log(f"[GM] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = eas.get_all_level_actors()

# World Settings GameMode override
ws = None
for a in actors:
    if "WorldSettings" in a.get_class().get_name():
        ws = a; break
if ws:
    gm = ws.get_editor_property("game_mode_override")
    L(f"WorldSettings.game_mode_override = {gm.get_name() if gm else 'None (usa project default)'}")

# project default gamemode (DefaultEngine.ini ja vimos = BP_AliceGameMode)
gm_bp = unreal.load_asset("/Game/Alice/Blueprints/BP_AliceGameMode")
if gm_bp:
    cdo = unreal.get_default_object(gm_bp.generated_class())
    dpc = cdo.get_editor_property("default_pawn_class")
    L(f"BP_AliceGameMode.default_pawn_class = {dpc.get_path_name() if dpc else None}")

# tem BP_Alice colocado no level? PlayerStart?
ps=0; alice_placed=0
for a in actors:
    cn = a.get_class().get_name()
    if "PlayerStart" in cn: ps+=1
    if "Alice" in cn and "GameMode" not in cn:
        alice_placed+=1
        L(f"  Alice actor no level: {cn} '{a.get_actor_label()}' at {a.get_actor_location()}")
L(f"PlayerStarts={ps}  Alice actors colocados={alice_placed}")
L("END")
