"""Procura CameraActor/CineCamera no L_Arena que rouba a view + confirma GameMode pawn."""
import unreal
L = lambda s: unreal.log(f"[LC] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Arena")
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
cams=0; ps=0; alice=0
for a in eas.get_all_level_actors():
    cn=a.get_class().get_name()
    if "Camera" in cn:
        cams+=1
        try: aa=a.get_editor_property("auto_activate_for_player")
        except: aa="?"
        L(f"CAM: {cn} '{a.get_actor_label()}' auto_activate={aa}")
    if "PlayerStart" in cn: ps+=1
    if "Alice" in cn and "GameMode" not in cn:
        alice+=1; L(f"Alice placed: {cn} '{a.get_actor_label()}'")
L(f"cams={cams} playerstarts={ps} alice_placed={alice}")

# WorldSettings gamemode
ws=None
for a in eas.get_all_level_actors():
    if "WorldSettings" in a.get_class().get_name(): ws=a; break
gm=ws.get_editor_property("default_game_mode") if ws else None
L(f"L_Arena WorldSettings GM={gm.get_name() if gm else 'None (usa global)'}")

# global GM default pawn
gmbp=unreal.load_asset("/Game/Alice/Blueprints/BP_AliceGameMode")
if gmbp:
    gcdo=unreal.get_default_object(gmbp.generated_class())
    dpc=gcdo.get_editor_property("default_pawn_class")
    L(f"GM.default_pawn = {dpc.get_name() if dpc else None}")
L("END")
