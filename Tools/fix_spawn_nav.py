"""Diag terreno + corrige PlayerStart (encontra Z real do chao) + rebuild nav."""
import unreal
L=lambda s:unreal.log(f"[FS] {s}")

unreal.EditorLoadingAndSavingUtils.load_map("/Game/Alice/Maps/L_MundoIlha")
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
acts=eas.get_all_level_actors()

# acha T_interior
ti=None
for a in acts:
    if a.get_actor_label()=="SM_Ilha_T_interior":
        ti=a; break
if ti:
    o,e=ti.get_actor_bounds(False)
    L(f"T_interior centro=({o.x/100:.0f},{o.y/100:.0f},{o.z/100:.0f})m ext=({e.x/100:.0f},{e.y/100:.0f},{e.z/100:.0f})m")
    # max Z do terreno
    top_z = o.z + e.z
    L(f"top Z do interior = {top_z/100:.1f}m")
    # move PlayerStart pra cima do centro do interior
    for a in acts:
        if "PlayerStart" in a.get_class().get_name():
            new_loc = unreal.Vector(o.x, o.y, top_z + 500)  # 5m acima
            a.set_actor_location(new_loc, False, False)
            L(f"PlayerStart -> ({new_loc.x/100:.0f},{new_loc.y/100:.0f},{new_loc.z/100:.0f})m")
            break

# bounds totais da ilha (todos terrenos)
all_mins=[]; all_maxs=[]
for a in acts:
    cn=a.get_class().get_name()
    if "StaticMesh" not in cn or "PostProcess" in cn: continue
    try:
        o,e=a.get_actor_bounds(False)
        all_mins.append((o.x-e.x,o.y-e.y,o.z-e.z))
        all_maxs.append((o.x+e.x,o.y+e.y,o.z+e.z))
    except: pass
if all_mins:
    minx=min(m[0] for m in all_mins); miny=min(m[1] for m in all_mins); minz=min(m[2] for m in all_mins)
    maxx=max(m[0] for m in all_maxs); maxy=max(m[1] for m in all_maxs); maxz=max(m[2] for m in all_maxs)
    L(f"ilha total: X[{minx/100:.0f},{maxx/100:.0f}] Y[{miny/100:.0f},{maxy/100:.0f}] Z[{minz/100:.0f},{maxz/100:.0f}]m")
    # nav: cobre tudo + folga
    cx=(minx+maxx)/2; cy=(miny+maxy)/2; cz=(minz+maxz)/2
    sx=(maxx-minx)/100+50; sy=(maxy-miny)/100+50; sz=(maxz-minz)/100+30
    # remove nav antigo, recria com bounds certos
    for a in acts:
        if "NavMeshBounds" in a.get_class().get_name(): eas.destroy_actor(a)
    nav=eas.spawn_actor_from_class(unreal.NavMeshBoundsVolume, unreal.Vector(cx,cy,cz))
    nav.set_actor_scale3d(unreal.Vector(sx, sy, sz))
    nav.set_actor_label("WorldNav")
    L(f"NavBounds centro=({cx/100:.0f},{cy/100:.0f},{cz/100:.0f}) scale=({sx:.0f},{sy:.0f},{sz:.0f})")

unreal.EditorLoadingAndSavingUtils.save_current_level()
unreal.SystemLibrary.execute_console_command(None, "RebuildNavigation")
L("salvo + nav rebuild disparado")
L("END")
