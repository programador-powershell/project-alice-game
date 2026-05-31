"""Com PIE rodando: acha o player pawn, le transform de um bone agora.
Rode 2x com intervalo pra comparar = prova de animacao real no jogo."""
import unreal
L = lambda s: unreal.log(f"[PB] {s}")

# acha o mundo PIE
worlds = unreal.EditorLevelLibrary.get_all_level_actors() if False else None
pie_world = None
for w in unreal.EditorLevelLibrary.get_editor_world().get_world() if False else []:
    pass

# metodo correto: pega game world via GameplayStatics
try:
    # em PIE, get_all_level_actors do EditorActorSubsystem pega editor; precisa do PIE world
    import unreal as u
    # itera worlds
    gi = None
    pawn = None
    # acha actor BP_Alice no PIE
    eas = u.get_editor_subsystem(u.EditorActorSubsystem)
    actors = eas.get_all_level_actors()
    for a in actors:
        cn = a.get_class().get_name()
        if "Alice" in cn and "Character" in cn or cn=="BP_Alice_C":
            pawn = a; break
    L(f"pawn(editor view)={pawn.get_class().get_name() if pawn else None}")
    if pawn:
        comp = pawn.get_component_by_class(u.SkeletalMeshComponent)
        if comp:
            for bn in ("LeftLeg","mixamorig:LeftLeg","LeftUpLeg","mixamorig:LeftUpLeg","RightHand","Spine1"):
                try:
                    tr = comp.get_bone_transform(bn)
                    loc = tr.translation
                    L(f"  bone {bn} = ({loc.x:.2f},{loc.y:.2f},{loc.z:.2f})")
                except Exception:
                    pass
except Exception as e:
    L(f"err {e}")
L("END")
