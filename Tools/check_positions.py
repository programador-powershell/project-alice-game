"""Mede posicao de cada Road (centro) = prova se areas espalhadas ou empilhadas.
Road vai de area A pra B, entao a posicao das roads revela o layout."""
import unreal
L=lambda s:unreal.log(f"[CP] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for a in eas.get_all_level_actors():
    lb=a.get_actor_label()
    if lb.startswith("Road_") or lb=="WorldBase":
        loc=a.get_actor_location()
        scl=a.get_actor_scale3d()
        L(f"{lb}: pos=({loc.x/100:.0f},{loc.y/100:.0f})m scale=({scl.x:.1f},{scl.y:.1f},{scl.z:.1f})")
L("END")
