"""Abre L_Mundo, conta sublevels, mede bounds total, poe PlayerStart no Interior (inicio)."""
import unreal
L = lambda s: unreal.log(f"[VW] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_Mundo")
w = unreal.EditorLevelLibrary.get_editor_world()
levels = unreal.EditorLevelUtils.get_levels(w)
L(f"sublevels carregados = {len(levels)}")

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = eas.get_all_level_actors()
# bounds total do mundo
minx=miny=1e9; maxx=maxy=-1e9; mesh=0
for a in actors:
    cn=a.get_class().get_name()
    if any(t in cn for t in ("Light","Sky","PostProcess","Fog","Atmosphere")): continue
    try:
        o,e=a.get_actor_bounds(False)
        if e.x<1: continue
        minx=min(minx,o.x-e.x);maxx=max(maxx,o.x+e.x)
        miny=min(miny,o.y-e.y);maxy=max(maxy,o.y+e.y);mesh+=1
    except: pass
L(f"mundo bounds: {(maxx-minx)/100:.0f}m x {(maxy-miny)/100:.0f}m, meshes={mesh}")

# PlayerStart no Interior (-500,0)m
ps=None
for a in actors:
    if "PlayerStart" in a.get_class().get_name(): ps=a; break
if ps:
    ps.set_actor_location(unreal.Vector(-50000,0,200), False, False)
    L(f"PlayerStart movido p/ Interior")
else:
    ps = eas.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(-50000,0,200))
    L("PlayerStart criado no Interior")

unreal.EditorLoadingAndSavingUtils.save_current_level()
L("L_Mundo salvo c/ PlayerStart")
L("END")
