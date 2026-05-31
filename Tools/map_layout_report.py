"""Relatorio do layout do L_Mundo: posicao+bounds de cada area + roads + gaps.
Prova se areas estao ligadas (roads cobrem) ou isoladas. Nao depende de render."""
import unreal
L=lambda s:unreal.log(f"[ML] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors=eas.get_all_level_actors()

# agrupa por area (label prefix) + roads
areas={}; roads=[]; base=None
for a in actors:
    lb=a.get_actor_label(); cn=a.get_class().get_name()
    if lb.startswith("Road_"): roads.append(lb)
    elif lb=="WorldBase": base=a
    # actors de mesh com bounds
for a in actors:
    cn=a.get_class().get_name()
    if any(t in cn for t in ("Light","Sky","PostProcess","Fog","Atmosphere","PlayerStart","Nav","Brush")): continue
    try:
        o,e=a.get_actor_bounds(False)
        if e.x<50 and e.y<50: continue
    except: continue

# conta por tipo
L(f"roads={len(roads)}: {roads}")
L(f"WorldBase: {'SIM' if base else 'NAO'}")
if base:
    o,e=base.get_actor_bounds(False)
    L(f"  base centro=({o.x/100:.0f},{o.y/100:.0f}) tam=({e.x*2/100:.0f}x{e.y*2/100:.0f})m")

# sublevels via streaming
w=unreal.EditorLevelLibrary.get_editor_world()
ss=w.get_editor_property("streaming_levels") if hasattr(w,'get_editor_property') else []
L(f"streaming_levels={len(ss) if ss else 0}")
for s in (ss or []):
    try:
        nm=s.get_world_asset().get_asset_name() if hasattr(s,'get_world_asset') else str(s)
        tr=s.get_editor_property("level_transform") if hasattr(s,'get_editor_property') else None
        loc=tr.translation if tr else None
        L(f"  SUB {nm} @ ({loc.x/100:.0f},{loc.y/100:.0f},{loc.z/100:.0f})m" if loc else f"  SUB {nm}")
    except Exception as e:
        L(f"  sub err {e}")
L("END")
