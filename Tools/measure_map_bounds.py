"""Mede bounds (XY) de cada L_* area. Usado pra auto-layout sem sobreposicao."""
import unreal
L = lambda s: unreal.log(f"[MB] {s}")

areas = ["L_InteriorDeCha","L_Vortice","L_TocaMecanica","L_Arena","L_FlorestaCheshire",
         "L_SalaoCha","L_NevoaCogumelos","L_PatioReal","L_Ruinas","L_CampoEtereo"]
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

for a in areas:
    unreal.EditorLoadingAndSavingUtils.load_map(f"/Game/Alice/Maps/{a}")
    actors = eas.get_all_level_actors()
    minx=miny=1e9; maxx=maxy=-1e9; n=0
    for ac in actors:
        # ignora luzes/sky/postprocess que nao definem footprint
        cn = ac.get_class().get_name()
        if any(t in cn for t in ("Light","Sky","PostProcess","PlayerStart","Fog","Atmosphere")): continue
        try:
            o,e = ac.get_actor_bounds(False)
            if e.x<1 and e.y<1: continue
            minx=min(minx,o.x-e.x); maxx=max(maxx,o.x+e.x)
            miny=min(miny,o.y-e.y); maxy=max(maxy,o.y+e.y); n+=1
        except Exception: pass
    if n>0:
        w=(maxx-minx)/100.0; h=(maxy-miny)/100.0  # cm->m
        cx=(minx+maxx)/2/100.0; cy=(miny+maxy)/2/100.0
        L(f"{a}: W={w:.0f}m H={h:.0f}m centro=({cx:.0f},{cy:.0f}) actors={n}")
    else:
        L(f"{a}: VAZIO")
L("END")
